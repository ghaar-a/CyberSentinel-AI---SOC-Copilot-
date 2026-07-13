from src.interfaces.llm_provider import LLMProvider
from src.interfaces.prompt_provider import PromptProvider
from src.retrieval.retriever import Retriever

from src.utils.logger import logger


class CyberSentinelAgent:
    """
    Agente principal do CyberSentinel AI.

    Responsável apenas por orquestrar
    o fluxo entre recuperação,
    construção do prompt e execução do LLM.
    """

    def __init__(
        self,
        retriever: Retriever,
        prompt_provider: PromptProvider,
        llm_provider: LLMProvider,
    ) -> None:

        self.retriever = retriever
        self.prompt_provider = prompt_provider
        self.llm_provider = llm_provider

    def ask(
        self,
        question: str,
    ) -> str:

        logger.info(
            "Recebida nova pergunta."
        )

        retrieved_chunks = self.retriever.retrieve(
            query=question
        )

        prompt = self.prompt_provider.build_prompt(
            user_question=question,
            retrieved_chunks=retrieved_chunks,
        )

        response = self.llm_provider.generate(
            prompt
        )

        logger.info(
            "Resposta gerada."
        )

        return response