from __future__ import annotations

from src.embedding.embedding_generator import EmbeddingGenerator
from src.interfaces.vector_store import VectorStore
from src.vectorstore.vector_document import VectorDocument
from src.utils.logger import logger


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
        chunks,
    ) -> None:
        """
        Gera embeddings e indexa os chunks no VectorStore.

        O índice existente é limpo antes da indexação para garantir
        que uma reconstrução da Base de Conhecimento não gere
        documentos duplicados.

        Args:
            chunks:
                Chunks provenientes da Base de Conhecimento.
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

        self._vector_store.clear()

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

        self._vector_store.add_many(
            vector_documents,
        )

        logger.info(
            "Indexação concluída. %d documentos vetoriais disponíveis.",
            self._vector_store.size(),
        )