from __future__ import annotations

from pathlib import Path

from src.chunking.markdown_chunker import MarkdownChunker
from src.embedding.embedding_generator import EmbeddingGenerator
from src.embedding.sentence_transformers_embedding_provider import (
    SentenceTransformersEmbeddingProvider,
)
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.retrieval.retrieved_chunk import RetrievedChunk
from src.retrieval.vector_retriever import VectorRetriever
from src.vectorstore.in_memory_vector_store import (
    InMemoryVectorStore,
)


def test_rag_pipeline_end_to_end() -> None:
    """
    Valida o pipeline RAG completo.

    O teste executa o fluxo:

    Documentos
        ↓
    KnowledgeLoader
        ↓
    MarkdownChunker
        ↓
    EmbeddingGenerator
        ↓
    VectorStore
        ↓
    VectorRetriever
        ↓
    RetrievedChunk

    O teste não utiliza o Gemini, pois o objetivo é validar
    a recuperação semântica e a indexação de forma determinística,
    sem depender de uma API externa.
    """

    knowledge_directory = Path(
        "data/knowledge"
    )

    loader = KnowledgeLoader(
        knowledge_directory=knowledge_directory
    )

    loader.load()

    documents = loader.get_all()

    assert documents, (
        "A base de conhecimento não possui documentos."
    )

    chunker = MarkdownChunker(
        repository=loader
    )

    chunks = chunker.get_chunks()

    assert chunks, (
        "Nenhum chunk foi gerado a partir da base de conhecimento."
    )

    embedding_provider = (
        SentenceTransformersEmbeddingProvider(
            model_name="all-MiniLM-L6-v2"
        )
    )

    embedding_generator = EmbeddingGenerator(
        provider=embedding_provider
    )

    embeddings = embedding_generator.generate(
        chunks
    )

    assert len(embeddings) == len(chunks)

    assert all(
        embedding.vector
        for embedding in embeddings
    )

    vector_store = InMemoryVectorStore()

    vector_documents = [
        embedding_provider.to_vector_document(
            embedding
        )
        for embedding in embeddings
    ]

    vector_store.add_many(
        vector_documents
    )

    assert vector_store.size() == len(
        vector_documents
    )

    retriever = VectorRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    query = (
        "Quais são as limitações do assistente "
        "e o que ele não deve fazer?"
    )

    results = retriever.retrieve(
        query=query,
        limit=3,
    )

    assert results, (
        "A busca semântica não retornou resultados."
    )

    assert len(results) <= 3

    assert all(
        isinstance(
            result,
            RetrievedChunk,
        )
        for result in results
    )

    assert all(
        result.rank > 0
        for result in results
    )

    assert all(
        result.chunk.content
        for result in results
    )

    assert results[0].rank == 1

    print(
        "\nResultados da busca semântica:"
    )

    for result in results:

        print(
            f"\nRank: {result.rank}"
        )

        print(
            f"Score: {result.score:.4f}"
        )

        print(
            f"Documento: "
            f"{result.chunk.document_name}"
        )

        print(
            f"Conteúdo: "
            f"{result.chunk.content[:200]}..."
        )