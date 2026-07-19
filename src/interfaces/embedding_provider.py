from __future__ import annotations

from abc import ABC, abstractmethod

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding


class EmbeddingProvider(ABC):
    """
    Contrato para provedores de embeddings.

    A interface permite substituir a tecnologia responsável
    pela geração dos vetores sem alterar as camadas superiores.

    Exemplos de implementações:

    - Sentence Transformers;
    - Google Gemini Embeddings;
    - OpenAI Embeddings;
    - Outros modelos compatíveis.
    """

    @abstractmethod
    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        """
        Gera embeddings para uma coleção de chunks.

        Args:
            chunks:
                Chunks que serão transformados em vetores.

        Returns:
            Lista de embeddings gerados.
        """

        raise NotImplementedError