from src.agent.cyber_sentinel_agent import CyberSentinelAgent
from src.chunking.markdown_chunker import MarkdownChunker
from src.config.settings import (
    CHROMA_DIR,
    PROMPTS_DIR,
    settings,
)
from src.embedding.embedding_generator import EmbeddingGenerator
from src.embedding.sentence_transformers_embedding_provider import (
    SentenceTransformersEmbeddingProvider,
)
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.llm.gemini_client import GeminiClient
from src.prompts.prompt_manager import PromptManager
from src.retrieval.retriever import Retriever
from src.retrieval.vector_retriever import VectorRetriever
from src.utils.logger import logger
from src.vectorstore.chroma_vector_store import ChromaVectorStore
from src.vectorstore.vector_document import VectorDocument


def create_agent() -> CyberSentinelAgent:
    """
    Inicializa todos os componentes necessários para o CyberSentinel AI.

    O pipeline utiliza recuperação semântica persistente através
    de Sentence Transformers e ChromaDB.
    """

    logger.info(
        "Inicializando base de conhecimento..."
    )

    knowledge_loader = KnowledgeLoader()

    knowledge_loader.load()

    logger.info(
        "Criando chunks da base de conhecimento..."
    )

    chunker = MarkdownChunker(
        repository=knowledge_loader,
    )

    chunks = chunker.get_chunks()

    logger.info(
        "Chunks disponíveis: %d",
        len(chunks),
    )

    embedding_provider = SentenceTransformersEmbeddingProvider(
        model_name=settings.embedding_model,
    )

    embedding_generator = EmbeddingGenerator(
        provider=embedding_provider,
    )

    logger.info(
        "Gerando embeddings da base de conhecimento..."
    )

    embeddings = embedding_generator.generate(
        chunks,
    )

    vector_documents = [
        VectorDocument(
            id=embedding.chunk.id,
            chunk=embedding.chunk,
            vector=embedding.vector,
        )
        for embedding in embeddings
    ]

    vector_store = ChromaVectorStore(
        persist_directory=str(
            CHROMA_DIR,
        ),
        collection_name=settings.chroma_collection_name,
    )

    vector_store.add_many(
        vector_documents,
    )

    logger.info(
        "Índice vetorial disponível com %d documentos.",
        vector_store.size(),
    )

    vector_retriever = VectorRetriever(
        embedding_generator=embedding_generator,
        vector_store=vector_store,
    )

    retriever = Retriever(
        strategy=vector_retriever,
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

        try:

            response = agent.ask(
                question,
            )

            print(
                "\nResposta:\n"
            )

            print(
                response,
            )

        except Exception as exception:

            logger.exception(
                "Erro ao processar a pergunta: %s",
                exception,
            )

            print(
                "\nNão foi possível processar sua solicitação."
            )


if __name__ == "__main__":
    main()