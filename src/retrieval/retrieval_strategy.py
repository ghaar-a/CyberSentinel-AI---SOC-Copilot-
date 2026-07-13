from __future__ import annotations

from abc import ABC, abstractmethod

from src.retrieval.retrieved_chunk import RetrievedChunk


class RetrievalStrategy(ABC):
    """
    Contrato para estratégias de recuperação.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError