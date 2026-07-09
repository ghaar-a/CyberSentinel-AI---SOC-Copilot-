# O Agent é o orquestrador principal do fluxo de execução do CyberSentinel AI.
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.prompts.prompt_manager import PromptManager
from src.llm.gemini_client import GeminiClient

from src.utils.logger import logger


class CyberSentinelAgent:
    """
    Agente principal do CyberSentinel AI.

    Responsável por coordenar o fluxo
    completo entre:

    - Base de Conhecimento
    - Prompt Engine
    - Gemini
    """

    def __init__(
        self,
        knowledge_loader: KnowledgeLoader,
        prompt_manager: PromptManager,
        llm_client: GeminiClient
    ):

        self.knowledge_loader = knowledge_loader

        self.prompt_manager = prompt_manager

        self.llm_client = llm_client

    def ask(
        self,
        question: str
    ) -> str:

        logger.info(
            "Nova pergunta recebida."
        )

        documents = (
            self.knowledge_loader.search(
                question
            )
        )

        prompt = (
            self.prompt_manager.build_prompt(
                user_question=question,
                documents=documents
            )
        )

        response = (
            self.llm_client.generate(
                prompt
            )
        )

        logger.info(
            "Resposta entregue ao usuário."
        )

        return response