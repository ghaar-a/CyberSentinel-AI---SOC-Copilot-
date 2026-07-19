from __future__ import annotations

from src.chunking.chunk import Chunk
from src.embedding.embedding_generator import EmbeddingGenerator
from src.interfaces.vector_store import VectorStore
from src.vectorstore.vector_document import VectorDocument


class VectorIndexer:
    """
    Responsável por transformar chunks em documentos vetoriais
    e armazená-los no VectorStore.

    O fluxo realizado pelo indexador é:

    Chunk
        ↓
    EmbeddingGenerator
        ↓
    Embedding
        ↓
    VectorDocument
        ↓
    VectorStore

    O indexador depende apenas da abstração VectorStore.
    Dessa forma, a implementação concreta do armazenamento
    pode ser substituída sem alterar esta classe.
    """

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
    ) -> None:
        """
        Inicializa o indexador vetorial.

        Args:
            embedding_generator:
                Componente responsável pela geração dos embeddings.

            vector_store:
                Armazenamento vetorial responsável pela indexação.
        """

        self._embedding_generator = (
            embedding_generator
        )

        self._vector_store = (
            vector_store
        )

    def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """
        Gera embeddings e indexa os chunks.

        Args:
            chunks:
                Chunks que serão transformados e indexados.
        """

        if not chunks:
            return

        embeddings = (
            self._embedding_generator.generate(
                chunks,
            )
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

    def clear(
        self,
    ) -> None:
        """
        Remove todos os documentos do índice vetorial.
        """

        self._vector_store.clear()

    def size(
        self,
    ) -> int:
        """
        Retorna a quantidade de documentos atualmente indexados.
        """

        return self._vector_store.size()