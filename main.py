from src.agent.cyber_sentinel_agent import CyberSentinelAgent

from src.chunking import MarkdownChunker

from src.config.settings import (
    PROMPTS_DIR,
)

from src.embedding import (
    EmbeddingGenerator,
    SentenceTransformersEmbeddingProvider,
)

from src.indexing.vector_indexer import VectorIndexer

from src.knowledge.knowledge_loader import (
    KnowledgeLoader,
)

from src.llm.gemini_client import (
    GeminiClient,
)

from src.prompts.prompt_manager import (
    PromptManager,
)

from src.retrieval import (
    Retriever,
    VectorRetriever,
)

from src.vectorstore import (
    InMemoryVectorStore,
)

from src.utils.logger import logger


EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


def create_agent() -> CyberSentinelAgent:
    """
    Inicializa todos os componentes necessários
    para o CyberSentinel AI.

    O processo de inicialização realiza:

    1. Carregamento da base de conhecimento.
    2. Divisão dos documentos em chunks.
    3. Geração dos embeddings dos chunks.
    4. Indexação dos vetores.
    5. Configuração do recuperador vetorial.
    6. Configuração da Prompt Engine.
    7. Configuração do cliente LLM.

    Returns:
        Agente CyberSentinel AI configurado.
    """

    logger.info(
        "Inicializando base de conhecimento..."
    )

    knowledge_loader = (
        KnowledgeLoader()
    )

    knowledge_loader.load()

    logger.info(
        "Base de conhecimento carregada: %d documentos.",
        len(
            knowledge_loader.documents
        ),
    )

    logger.info(
        "Gerando chunks da base de conhecimento..."
    )

    chunker = MarkdownChunker(
        repository=knowledge_loader,
    )

    chunks = chunker.get_chunks()

    logger.info(
        "Chunks gerados: %d.",
        len(chunks),
    )

    logger.info(
        "Inicializando modelo de embeddings: %s",
        EMBEDDING_MODEL,
    )

    embedding_provider = (
        SentenceTransformersEmbeddingProvider(
            model_name=EMBEDDING_MODEL,
        )
    )

    embedding_generator = (
        EmbeddingGenerator(
            provider=embedding_provider,
        )
    )

    vector_store = (
        InMemoryVectorStore()
    )

    vector_indexer = (
        VectorIndexer(
            embedding_generator=embedding_generator,
            vector_store=vector_store,
        )
    )

    logger.info(
        "Indexando chunks no armazenamento vetorial..."
    )

    vector_indexer.index(
        chunks,
    )

    logger.info(
        "Indexação vetorial concluída: %d documentos.",
        vector_indexer.size(),
    )

    vector_retriever = (
        VectorRetriever(
            embedding_generator=embedding_generator,
            vector_store=vector_store,
        )
    )

    retriever = (
        Retriever(
            strategy=vector_retriever,
        )
    )

    prompt_manager = (
        PromptManager(
            prompts_directory=PROMPTS_DIR,
        )
    )

    gemini_client = (
        GeminiClient()
    )

    return CyberSentinelAgent(
        retriever=retriever,
        prompt_provider=prompt_manager,
        llm_provider=gemini_client,
    )


def main() -> None:
    """
    Executa a aplicação interativa do CyberSentinel AI.
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

        if question.lower() in [
            "exit",
            "quit",
            "sair",
        ]:
            logger.info(
                "Encerrando aplicação."
            )

            break

        if not question:
            continue

        try:

            response = agent.ask(
                question,
            )

            print(
                "\nResposta:\n"
            )

            print(
                response
            )

        except Exception as exc:

            logger.exception(
                "Erro ao processar pergunta: %s",
                exc,
            )

            print(
                "\nNão foi possível processar "
                "a pergunta. Consulte os logs "
                "para mais detalhes."
            )


if __name__ == "__main__":
    main()