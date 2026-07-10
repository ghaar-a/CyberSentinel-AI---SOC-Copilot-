from __future__ import annotations

from abc import ABC, abstractmethod

from src.knowledge.knowledge_document import KnowledgeDocument


class RetrievalStrategy(ABC):
    """
    Define o contrato para qualquer estratégia
    de recuperação de documentos.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        limit: int = 5
    ) -> list[KnowledgeDocument]:
        raise NotImplementedError