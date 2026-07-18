from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.interfaces.embedding_provider import EmbeddingProvider


class SentenceTransformersEmbeddingProvider(EmbeddingProvider):
    """
    Implementação concreta responsável pela geração de embeddings
    utilizando Sentence Transformers.

    Esta classe é utilizada durante a etapa de indexação da base
    de conhecimento e permanece desacoplada da camada de Retrieval.

    O modelo pode ser alterado futuramente sem impactar o restante
    da aplicação.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        """
        Inicializa o modelo de embeddings.

        Args:
            model_name:
                Nome do modelo Sentence Transformers.
        """

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
            Lista de Embeddings.
        """

        if not chunks:
            return []

        vectors = self._model.encode(
            [chunk.content for chunk in chunks],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
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