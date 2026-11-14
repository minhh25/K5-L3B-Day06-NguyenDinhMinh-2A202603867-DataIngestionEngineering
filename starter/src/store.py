
import math
from collections import defaultdict
from typing import Any

import psycopg
from psycopg import sql
from psycopg.types.json import Jsonb

from .models import Chunk


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int) -> None:
        if not database_url:
            raise ValueError("database_url must not be empty")

        if not isinstance(dimensions, int) or not 1 <= dimensions <= 16000:
            raise ValueError("Invalid embedding dimensions")

        self.database_url = database_url
        self.dimensions = dimensions

    def create_schema(self) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

                cur.execute(
                    sql.SQL("""
                        CREATE TABLE IF NOT EXISTS lab_chunks (
                            strategy TEXT NOT NULL,
                            chunk_id TEXT NOT NULL,
                            document_id TEXT NOT NULL,
                            source TEXT NOT NULL,
                            page INTEGER NOT NULL,
                            text TEXT NOT NULL,
                            metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                            embedding vector({}) NOT NULL,
                            PRIMARY KEY (strategy, chunk_id)
                        )
                    """).format(sql.SQL(str(self.dimensions)))
                )

                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_lab_chunks_strategy
                    ON lab_chunks (strategy)
                """)

                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_lab_chunks_document
                    ON lab_chunks (strategy, document_id)
                """)

                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_lab_chunks_source_page
                    ON lab_chunks (source, page)
                """)
                cur.execute("""
                    SELECT format_type(atttypid, atttypmod)
                    FROM pg_attribute
                    WHERE attrelid = 'lab_chunks'::regclass
                      AND attname = 'embedding'
                """)
                if cur.fetchone()[0] != f"vector({self.dimensions})":
                    raise ValueError("Stored vector dimensions differ from the embedding model")

    def _validate_vector(self, vector: list[float]) -> None:
        if len(vector) != self.dimensions:
            raise ValueError(
                f"Expected {self.dimensions} dimensions, got {len(vector)}"
            )

        if not all(math.isfinite(float(value)) for value in vector):
            raise ValueError("Vector contains non-finite values")

    def upsert(
        self,
        strategy: str,
        chunks: list[Chunk],
        vectors: list[list[float]]
    ) -> None:
        if not strategy or not strategy.strip():
            raise ValueError("Strategy must not be empty")

        if len(chunks) != len(vectors):
            raise ValueError("Chunks and vectors must have equal lengths")

        if not chunks:
            return

        document_chunks = defaultdict(list)
        seen_ids = set()

        for chunk, vector in zip(chunks, vectors):
            self._validate_vector(vector)

            if not chunk.chunk_id or not chunk.document_id:
                raise ValueError("Invalid chunk ID or document ID")

            if not chunk.text.strip():
                raise ValueError("Chunk text must not be empty")

            if chunk.chunk_id in seen_ids:
                raise ValueError(f"Duplicate chunk ID: {chunk.chunk_id}")

            seen_ids.add(chunk.chunk_id)
            document_chunks[chunk.document_id].append(chunk.chunk_id)

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                for chunk, vector in zip(chunks, vectors):
                    vector_string = "[" + ",".join(
                        str(float(value)) for value in vector
                    ) + "]"

                    cur.execute("""
                        INSERT INTO lab_chunks (
                            strategy,
                            chunk_id,
                            document_id,
                            source,
                            page,
                            text,
                            metadata,
                            embedding
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s::vector
                        )
                        ON CONFLICT (strategy, chunk_id)
                        DO UPDATE SET
                            document_id = EXCLUDED.document_id,
                            source = EXCLUDED.source,
                            page = EXCLUDED.page,
                            text = EXCLUDED.text,
                            metadata = EXCLUDED.metadata,
                            embedding = EXCLUDED.embedding
                    """, (
                        strategy,
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.source,
                        chunk.page,
                        chunk.text,
                        Jsonb(chunk.metadata),
                        vector_string
                    ))

                for document_id, chunk_ids in document_chunks.items():
                    cur.execute("""
                        DELETE FROM lab_chunks
                        WHERE strategy = %s
                          AND document_id = %s
                          AND NOT (chunk_id = ANY(%s))
                    """, (strategy, document_id, chunk_ids))

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        if not strategy or not strategy.strip():
            raise ValueError("Strategy must not be empty")

        self._validate_vector(query_vector)

        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        vector_string = "[" + ",".join(
            str(float(value)) for value in query_vector
        ) + "]"

        conditions = [sql.SQL("strategy = %s")]
        params = [strategy]

        allowed_columns = {"document_id", "source", "page"}

        for key, value in (filters or {}).items():
            if key in allowed_columns:
                conditions.append(
                    sql.SQL("{} = %s").format(sql.Identifier(key))
                )
                params.append(value)

            elif key == "metadata" and isinstance(value, dict):
                for metadata_key, metadata_value in value.items():
                    conditions.append(
                        sql.SQL("metadata ->> %s = %s")
                    )
                    params.extend([
                        metadata_key,
                        str(metadata_value).lower()
                        if isinstance(metadata_value, bool)
                        else str(metadata_value)
                    ])

            else:
                raise ValueError(f"Unsupported filter: {key}")

        where_clause = sql.SQL(" AND ").join(conditions)

        query = sql.SQL("""
            SELECT
                chunk_id,
                document_id,
                source,
                page,
                text,
                metadata,
                1 - (embedding <=> %s::vector) AS score
            FROM lab_chunks
            WHERE {}
            ORDER BY embedding <=> %s::vector, chunk_id
            LIMIT %s
        """).format(where_clause)

        query_params = [vector_string] + params + [
            vector_string,
            top_k
        ]

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query, query_params)
                rows = cur.fetchall()

        return [
            {
                "chunk_id": row[0],
                "document_id": row[1],
                "source": row[2],
                "page": row[3],
                "text": row[4],
                "metadata": row[5],
                "score": float(row[6])
            }
            for row in rows
        ]
