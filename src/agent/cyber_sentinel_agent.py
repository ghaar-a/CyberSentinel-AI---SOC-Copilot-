from src.interfaces.knowledge_provider import KnowledgeProvider
from src.interfaces.llm_provider import LLMProvider
from src.interfaces.prompt_provider import PromptProvider

from src.utils.logger import logger


class CyberSentinelAgent:
    """
    Agente principal do CyberSentinel AI.

    Responsável por coordenar o fluxo entre:

    - Provedor de Conhecimento
    - Gerenciador de Prompts
    - Modelo de Linguagem
    """

    def __init__(
        self,
        knowledge_provider: KnowledgeProvider,
        prompt_provider: PromptProvider,
        llm_provider: LLMProvider,
    ) -> None:

        self.knowledge_provider = knowledge_provider
        self.prompt_provider = prompt_provider
        self.llm_provider = llm_provider

    def ask(
        self,
        question: str
    ) -> str:

        logger.info(
            "Nova pergunta recebida."
        )

        documents = self.knowledge_provider.search(
            query=question
        )

        prompt = self.prompt_provider.build_prompt(
            user_question=question,
            documents=documents,
        )

        response = self.llm_provider.generate(
            prompt
        )

        logger.info(
            "Resposta entregue ao usuário."
        )

        return response