from __future__ import annotations

from abc import ABC, abstractmethod

from src.chunking.chunk import Chunk


class Chunker(ABC):
    """
    Define como documentos serão
    divididos em chunks.
    """

    @abstractmethod
    def chunk(self) -> list[Chunk]:
        raise NotImplementedError