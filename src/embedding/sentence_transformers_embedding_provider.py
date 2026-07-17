from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.interfaces.embedding_provider import EmbeddingProvider


class SentenceTransformersEmbeddingProvider(EmbeddingProvider):
    """
    Implementação responsável pela geração de embeddings utilizando
    a biblioteca Sentence Transformers.

    Esta implementação será utilizada por qualquer banco vetorial
    suportado pela aplicação (FAISS, ChromaDB, pgvector etc.).

    A classe permanece desacoplada da camada de recuperação,
    sendo utilizada apenas durante o processo de indexação.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self._model = SentenceTransformer(model_name)

    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        """
        Gera embeddings para uma coleção de chunks.

        Args:
            chunks:
                Chunks que serão vetorizados.

        Returns:
            Lista de embeddings correspondentes.
        """

        if not chunks:
            return []

        vectors = self._model.encode(
            [chunk.content for chunk in chunks],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings: list[Embedding] = []

        for chunk, vector in zip(chunks, vectors):

            embeddings.append(
                Embedding(
                    chunk=chunk,
                    vector=vector.tolist(),
                )
            )

        return embeddings