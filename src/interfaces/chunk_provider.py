from __future__ import annotations

from abc import ABC, abstractmethod

from src.chunking.chunk import Chunk


class ChunkProvider(ABC):
    """
    Contrato responsável por fornecer
    chunks para a aplicação.
    """

    @abstractmethod
    def get_chunks(self) -> list[Chunk]:
        raise NotImplementedError