from src.agent.cyber_sentinel_agent import CyberSentinelAgent
from src.config.settings import PROMPTS_DIR
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.llm.gemini_client import GeminiClient
from src.prompts.prompt_manager import PromptManager
from src.utils.logger import logger


from src.chunking import MarkdownChunker

from src.retrieval import Retriever
from src.retrieval.keyword_chunk_retriever import (
    KeywordChunkRetriever,
)

def create_agent() -> CyberSentinelAgent:
    """
    Inicializa todos os componentes
    necessários para o CyberSentinel AI.
    """

    knowledge_loader = KnowledgeLoader()

    knowledge_loader.load()

    chunker = MarkdownChunker(
        repository=knowledge_loader
    )

    chunker.chunk()

    retriever = Retriever(
        strategy=KeywordChunkRetriever(
            provider=chunker
    )
)

    chunker = MarkdownChunker(
        repository=knowledge_loader
    )

    chunker.chunk()

    prompt_manager = PromptManager(
        prompts_directory=PROMPTS_DIR
    )

    gemini_client = GeminiClient()

    return CyberSentinelAgent(
        retriever=retriever,
        prompt_manager=prompt_manager,
        llm_client=gemini_client,
    )


def main():

    logger.info(
        "Inicializando CyberSentinel AI..."
    )

    agent = create_agent()

    logger.info(
        "Agente iniciado com sucesso."
    )

    while True:

        question = input(
            "\nCyberSentinel > "
        )

        if question.lower() in [
            "exit",
            "quit",
            "sair"
        ]:
            logger.info(
                "Encerrando aplicação."
            )
            break


        response = agent.ask(
            question
        )


        print(
            "\nResposta:\n"
        )

        print(response)



if __name__ == "__main__":
    main()