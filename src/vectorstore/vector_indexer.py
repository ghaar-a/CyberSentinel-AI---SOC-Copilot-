from __future__ import annotations

from src.chunking.chunk import Chunk
from src.embedding.embedding_generator import EmbeddingGenerator
from src.interfaces.vector_store import VectorStore
from src.vectorstore.vector_document import VectorDocument


class VectorIndexer:
    """
    Responsável por transformar chunks em documentos vetoriais
    e enviá-los para a VectorStore.

    Esta classe representa o pipeline de indexação da aplicação.

    Fluxo:

    Chunk
        ↓
    EmbeddingGenerator
        ↓
    Embedding
        ↓
    VectorDocument
        ↓
    VectorStore
    """

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
    ) -> None:

        self._embedding_generator = embedding_generator
        self._vector_store = vector_store

    def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """
        Indexa uma coleção de chunks.

        Args:
            chunks:
                Chunks que serão armazenados no banco vetorial.
        """

        embeddings = self._embedding_generator.generate(chunks)

        documents: list[VectorDocument] = []

        for embedding in embeddings:

            chunk = embedding.chunk

            documents.append(
                VectorDocument(
                    id=chunk.id,
                    document_name=chunk.document_name,
                    category=chunk.category,
                    source_path=chunk.source_path,
                    chunk_index=chunk.index,
                    content=chunk.content,
                    embedding=embedding.vector,
                )
            )

        self._vector_store.add_many(documents)