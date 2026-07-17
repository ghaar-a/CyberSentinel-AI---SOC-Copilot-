from __future__ import annotations

from abc import ABC, abstractmethod

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding


class EmbeddingProvider(ABC):
    """
    Contrato para geração de embeddings.
    """

    @abstractmethod
    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        raise NotImplementedError