from __future__ import annotations

from abc import ABC, abstractmethod

from src.knowledge.knowledge_document import KnowledgeDocument


class DocumentRepository(ABC):
    """
    Contrato responsável por fornecer documentos
    para qualquer camada da aplicação.

    O repositório não define como os documentos
    são armazenados, apenas como são obtidos.
    """

    @abstractmethod
    def get_all(self) -> list[KnowledgeDocument]:
        """
        Retorna todos os documentos disponíveis.
        """
        raise NotImplementedError