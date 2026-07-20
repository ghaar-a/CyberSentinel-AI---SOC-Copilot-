from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.interfaces.embedding_provider import EmbeddingProvider
from src.utils.logger import logger


class SentenceTransformersEmbeddingProvider(EmbeddingProvider):
    """
    Implementação de EmbeddingProvider utilizando
    Sentence Transformers.

    O modelo é carregado uma única vez durante a criação
    do provider e reutilizado nas chamadas seguintes.

    Isso evita o custo de carregar novamente os pesos do modelo
    a cada geração de embedding.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        """
        Inicializa o provedor de embeddings.

        Args:
            model_name:
                Nome do modelo Sentence Transformers utilizado.
        """

        self._model_name = model_name

        logger.info(
            "Carregando modelo de embeddings: %s",
            model_name,
        )

        self._model = SentenceTransformer(
            model_name,
        )

        logger.info(
            "Modelo de embeddings carregado com sucesso.",
        )

    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        """
        Gera embeddings para os chunks informados.

        Args:
            chunks:
                Chunks que serão convertidos em vetores.

        Returns:
            Lista de embeddings associados aos chunks.
        """

        if not chunks:
            return []

        texts = [
            chunk.content
            for chunk in chunks
        ]

        vectors = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return [
            Embedding(
                chunk=chunk,
                vector=vector.tolist(),
            )
            for chunk, vector in zip(
                chunks,
                vectors,
            )
        ]