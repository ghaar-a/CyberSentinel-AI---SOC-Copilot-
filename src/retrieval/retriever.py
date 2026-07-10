from __future__ import annotations

from src.knowledge.knowledge_document import KnowledgeDocument

from src.retrieval.retrieval_strategy import RetrievalStrategy


class Retriever:
    """
    Fachada responsável por executar
    a estratégia de recuperação.
    """

    def __init__(
        self,
        strategy: RetrievalStrategy
    ) -> None:

        self.strategy = strategy

    def retrieve(
        self,
        query: str,
        limit: int = 5
    ) -> list[KnowledgeDocument]:

        return self.strategy.retrieve(
            query=query,
            limit=limit
        )