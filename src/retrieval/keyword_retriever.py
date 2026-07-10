from __future__ import annotations

from src.interfaces.document_repository import DocumentRepository
from src.knowledge.knowledge_document import KnowledgeDocument
from src.retrieval.retrieval_strategy import RetrievalStrategy


class KeywordRetriever(RetrievalStrategy):
    """
    Estratégia de recuperação baseada
    em palavras-chave.
    """

    def __init__(
        self,
        repository: DocumentRepository
    ) -> None:

        self.repository = repository

    def retrieve(
        self,
        query: str,
        limit: int = 5
    ) -> list[KnowledgeDocument]:

        terms = {
            term.lower()
            for term in query.split()
        }

        ranking: list[
            tuple[int, KnowledgeDocument]
        ] = []

        for document in self.repository.get_all():

            searchable_text = (
                f"{document.name}\n"
                f"{document.category}\n"
                f"{document.content}"
            ).lower()

            score = sum(
                term in searchable_text
                for term in terms
            )

            if score > 0:

                ranking.append(
                    (
                        score,
                        document
                    )
                )

        ranking.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            document
            for _, document
            in ranking[:limit]
        ]