from __future__ import annotations

from src.chunking.chunk import Chunk
from src.embedding.embedding_generator import EmbeddingGenerator
from src.interfaces.vector_store import VectorStore
from src.utils.logger import logger
from src.vectorstore.vector_document import VectorDocument


class KnowledgeIndexer:
    """
    Responsável por transformar a Base de Conhecimento
    em documentos vetoriais indexados.

    O processo executado é:

    Chunks
        ↓
    EmbeddingGenerator
        ↓
    Embeddings
        ↓
    VectorDocument
        ↓
    VectorStore

    Esta classe centraliza a responsabilidade de indexação,
    evitando que o código de inicialização da aplicação
    precise conhecer os detalhes desse processo.

    O indexador depende apenas das abstrações necessárias
    para geração de embeddings e armazenamento vetorial.
    Dessa forma, não possui conhecimento sobre a implementação
    concreta do VectorStore.
    """

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
    ) -> None:
        """
        Inicializa o indexador da Base de Conhecimento.

        Args:
            embedding_generator:
                Componente responsável pela geração dos embeddings.

            vector_store:
                Armazenamento responsável pela indexação dos vetores.
        """

        self._embedding_generator = embedding_generator
        self._vector_store = vector_store

    def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """
        Gera embeddings e indexa os chunks no VectorStore.

        O índice existente é limpo somente após a geração dos embeddings
        e a construção dos documentos vetoriais. Essa ordem evita que
        uma falha durante o processamento dos embeddings apague
        prematuramente um índice válido.

        Args:
            chunks:
                Lista de chunks provenientes da Base de Conhecimento.
        """

        if not chunks:
            logger.warning(
                "Nenhum chunk encontrado para indexação.",
            )
            return

        logger.info(
            "Iniciando indexação de %d chunks...",
            len(chunks),
        )

        embeddings = self._embedding_generator.generate(
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

        if not vector_documents:
            logger.warning(
                "Nenhum documento vetorial foi gerado para indexação.",
            )
            return

        self._vector_store.clear()

        self._vector_store.add_many(
            vector_documents,
        )

        logger.info(
            "Indexação concluída. %d documentos vetoriais disponíveis.",
            self._vector_store.size(),
        )