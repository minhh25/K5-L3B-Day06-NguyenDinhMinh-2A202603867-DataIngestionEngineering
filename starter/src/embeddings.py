
from typing import Protocol
from sentence_transformers import SentenceTransformer


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, question: str) -> list[float]:
        ...


class MyEmbedder:
    def __init__(self, model_name: str, revision: str | None = None) -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, revision=revision)
        self.dimensions = self.model.get_embedding_dimension()

        if self.dimensions is None:
            raise ValueError("Cannot determine embedding dimensions")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        inputs = [f"passage: {text}" for text in texts]

        vectors = self.model.encode(
            inputs,
            batch_size=16,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return vectors.tolist()

    def embed_query(self, question: str) -> list[float]:
        vector = self.model.encode(
            f"query: {question}",
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return vector.tolist()
