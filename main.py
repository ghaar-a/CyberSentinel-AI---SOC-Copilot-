from src.agent import CyberSentinelAgent
from src.chunking import MarkdownChunker
from src.config.settings import PROMPTS_DIR
from src.knowledge import KnowledgeLoader
from src.llm import GeminiClient
from src.prompts import PromptManager
from src.retrieval import KeywordChunkRetriever, Retriever
from src.utils import logger


def create_agent() -> CyberSentinelAgent:
    """
    Inicializa todos os componentes necessários
    para execução do CyberSentinel AI.
    """

    knowledge_loader = KnowledgeLoader()
    knowledge_loader.load()

    chunker = MarkdownChunker(
        repository=knowledge_loader,
    )

    chunker.chunk()

    retriever = Retriever(
        strategy=KeywordChunkRetriever(
            provider=chunker,
        )
    )

    prompt_manager = PromptManager(
        prompts_directory=PROMPTS_DIR,
    )

    gemini_client = GeminiClient()

    return CyberSentinelAgent(
        retriever=retriever,
        prompt_provider=prompt_manager,
        llm_provider=gemini_client,
    )


def main() -> None:
    """
    Ponto de entrada da aplicação.
    """

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
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
            "sair",
        }:
            logger.info(
                "Encerrando aplicação."
            )
            break

        if not question:
            continue

        response = agent.ask(
            question,
        )

        print("\nResposta:\n")
        print(response)


if __name__ == "__main__":
    main()