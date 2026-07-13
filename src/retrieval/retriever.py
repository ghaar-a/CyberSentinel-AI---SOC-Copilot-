from __future__ import annotations

from src.retrieval.retrieval_strategy import RetrievalStrategy
from src.retrieval.retrieved_chunk import RetrievedChunk


class Retriever:
    """
    Fachada responsável pela recuperação
    de contexto.
    """

    def __init__(
        self,
        strategy: RetrievalStrategy,
    ) -> None:

        self._strategy = strategy

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:

        return self._strategy.retrieve(
            query=query,
            limit=limit,
        )