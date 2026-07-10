from __future__ import annotations

from abc import ABC, abstractmethod

from src.knowledge.knowledge_document import KnowledgeDocument


class KnowledgeProvider(ABC):
    """
    Contrato para provedores de conhecimento.

    Qualquer implementação deve fornecer
    uma forma de pesquisar documentos.
    """

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 5
    ) -> list[KnowledgeDocument]:
        """
        Retorna documentos relevantes
        para a consulta.
        """
        raise NotImplementedError