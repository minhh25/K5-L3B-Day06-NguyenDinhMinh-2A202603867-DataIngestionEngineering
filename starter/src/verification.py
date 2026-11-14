from datetime import datetime
import hashlib
import json
import time
import uuid
from zoneinfo import ZoneInfo

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo

from .chunking import fixed_size
from .models import DocumentPage
from .store import PgVectorStore


def digest(rows):
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()


def inventory(store):
    with psycopg.connect(store.database_url) as conn:
        return conn.execute('SELECT strategy, chunk_id, document_id, source, page, text, metadata, embedding::text FROM lab_chunks ORDER BY strategy, chunk_id').fetchall()


def verify(store, embedder, expected):
    started = time.perf_counter()
    before = inventory(store)
    before_other = [r for r in before if r[0] not in expected]
    counts = {}
    coverage = {}
    for strategy, chunks in expected.items():
        rows = [r for r in before if r[0] == strategy]
        assert {r[1] for r in rows} == {c.chunk_id for c in chunks}, 'Stored IDs disagree with rebuilt IDs'
        previous = {r[1]: r for r in rows}
        for chunk in chunks:
            row = previous[chunk.chunk_id]
            assert (row[2],row[3],row[4],row[5]) == (chunk.document_id,chunk.source,chunk.page,chunk.text)
            assert row[6]['chapter'] == chunk.metadata['chapter']
            assert len(json.loads(row[7])) == 384
        for document_id, page in sorted({(c.document_id,c.page) for c in chunks}):
            items = [c for c in chunks if c.document_id == document_id and c.page == page]
            intervals = sorted((c.metadata['start_char'],c.metadata['end_char']) for c in items)
            coverage[f'{strategy}:{document_id}:{page}'] = intervals
        vectors = embedder.embed_documents([c.text for c in chunks])
        store.upsert(strategy, chunks, vectors)
        counts[strategy] = {'before': len(rows), 'expected': len(chunks), 'stable_ids': True,
                            'real_documents_reembedded': len(vectors)}
    after = inventory(store)
    for strategy in expected:
        ids_before = [r[1] for r in before if r[0] == strategy]
        ids_after = [r[1] for r in after if r[0] == strategy]
        assert ids_before == ids_after
        counts[strategy]['after'] = len(ids_after)
    assert digest(before_other) == digest([r for r in after if r[0] not in expected])
    schema = 'day6_verify_' + uuid.uuid4().hex[:12]
    with psycopg.connect(store.database_url) as conn:
        conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    isolated = PgVectorStore(make_conninfo(store.database_url, options=f'-csearch_path={schema},public'), 384)
    try:
        isolated.create_schema()
        page = DocumentPage('synthetic_revision_test', 'synthetic.txt', 1,
                            'Tài liệu thử nghiệm riêng. Kiểm tra việc thay đổi nguồn và xóa chunk lỗi thời. ' * 5)
        old_chunks = fixed_size(page, 100, 10)
        old_vectors = embedder.embed_documents([c.text for c in old_chunks])
        isolated.upsert('verification_only', old_chunks, old_vectors)
        isolated.upsert('verification_only', old_chunks, old_vectors)
        old_rows = inventory(isolated)
        assert len(old_rows) == len(old_chunks)
        page.text = 'Nguồn đã cập nhật. Nội dung mới chỉ còn một đoạn ngắn.'
        new_chunks = fixed_size(page, 100, 10)
        isolated.upsert('verification_only', new_chunks, embedder.embed_documents([c.text for c in new_chunks]))
        new_rows = inventory(isolated)
        assert len(new_rows) == 1 and new_rows[0][5] == page.text
        removed = sorted({c.chunk_id for c in old_chunks} - {r[1] for r in new_rows})
        assert len(removed) == len(old_chunks)-1
        change = {'schema_isolated': True, 'before_chunks': len(old_chunks),
                  'after_chunks': len(new_rows), 'removed_stale_ids': removed,
                  'same_id_updated_text': new_rows[0][1] == old_chunks[0].chunk_id,
                  'persistent_after_reconnect': True}
    finally:
        with psycopg.connect(store.database_url) as conn:
            conn.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))
    with psycopg.connect(store.database_url) as conn:
        duplicate_ids = conn.execute('SELECT strategy,chunk_id,count(*) FROM lab_chunks GROUP BY strategy,chunk_id HAVING count(*)>1').fetchall()
        dimension_counts = conn.execute('SELECT strategy,vector_dims(embedding),count(*) FROM lab_chunks GROUP BY 1,2 ORDER BY 1,2').fetchall()
        null_chapters = conn.execute("SELECT metadata->>'chapter',count(*) FROM lab_chunks WHERE strategy='paragraph_800' GROUP BY 1 ORDER BY 1").fetchall()
    assert not duplicate_ids
    return {'recorded_at': datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(),
            'production_idempotency': counts, 'duplicate_ids': duplicate_ids,
            'dimensions': dimension_counts, 'paragraph_chapters': null_chapters,
            'source_change_test': change, 'test_schema_cleaned': True,
            'extra_strategies_unchanged': True, 'production_source_pdf_modified': False,
            'metadata_matches_rebuilt': True, 'elapsed_seconds': time.perf_counter()-started,
            'page_chunk_spans': coverage,
            'durability_scope': 'Committed rows read via new connections; Docker volume separately inspected. Container restart not performed.'}
