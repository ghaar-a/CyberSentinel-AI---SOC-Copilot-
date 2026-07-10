from __future__ import annotations

from abc import ABC, abstractmethod

from src.knowledge.knowledge_document import KnowledgeDocument


class PromptProvider(ABC):
    """
    Contrato responsável pela construção
    do prompt final.
    """

    @abstractmethod
    def build_prompt(
        self,
        user_question: str,
        documents: list[KnowledgeDocument]
    ) -> str:
        """
        Constrói o prompt que será enviado ao LLM.
        """
        raise NotImplementedError