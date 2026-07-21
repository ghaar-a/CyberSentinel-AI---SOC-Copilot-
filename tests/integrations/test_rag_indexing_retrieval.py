"""
Testes de integração do pipeline de indexação e recuperação vetorial.

Esta suíte valida a integração entre:

    KnowledgeIndexer
        ↓
    EmbeddingGenerator
        ↓
    InMemoryVectorStore
        ↓
    VectorRetriever

Os testes utilizam embeddings determinísticos por meio de um mock,
permitindo validar o comportamento dos componentes de orquestração
sem depender de modelos externos ou de infraestrutura persistente.

O ChromaDB não é utilizado nesta suíte. A integração com o armazenamento
vetorial persistente será validada em testes de integração específicos.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.indexing.knowledge_indexer import KnowledgeIndexer
from src.retrieval.retrieved_chunk import RetrievedChunk
from src.retrieval.vector_retriever import VectorRetriever
from src.vectorstore.in_memory_vector_store import InMemoryVectorStore


# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def vector_store() -> InMemoryVectorStore:
    """
    Fornece uma instância isolada do armazenamento vetorial em memória.

    Uma nova instância é criada para cada teste, garantindo que os testes
    não compartilhem estado entre si.
    """

    return InMemoryVectorStore()


@pytest.fixture
def mock_embedding_generator() -> MagicMock:
    """
    Fornece um mock determinístico para geração de embeddings.

    O mock retorna o mesmo vetor para cada Chunk recebido. Isso permite
    validar a integração entre o indexador, o armazenamento vetorial
    e o recuperador sem depender de um modelo real de embeddings.
    """

    mock = MagicMock()

    default_vector = [
        0.1,
        0.2,
        0.3,
        0.4,
    ]

    mock.generate.side_effect = lambda chunks: [
        Embedding(
            chunk=chunk,
            vector=default_vector,
        )
        for chunk in chunks
    ]

    return mock


@pytest.fixture
def indexer(
    mock_embedding_generator: MagicMock,
    vector_store: InMemoryVectorStore,
) -> KnowledgeIndexer:
    """
    Cria uma instância do KnowledgeIndexer com dependências controladas.
    """

    return KnowledgeIndexer(
        embedding_generator=mock_embedding_generator,
        vector_store=vector_store,
    )


@pytest.fixture
def retriever(
    mock_embedding_generator: MagicMock,
    vector_store: InMemoryVectorStore,
) -> VectorRetriever:
    """
    Cria uma instância do VectorRetriever com dependências controladas.
    """

    return VectorRetriever(
        embedding_generator=mock_embedding_generator,
        vector_store=vector_store,
    )


# ==============================================================================
# TESTES DE INDEXAÇÃO
# ==============================================================================


def test_indexing_chunks_successfully(
    indexer: KnowledgeIndexer,
    vector_store: InMemoryVectorStore,
    mock_embedding_generator: MagicMock,
) -> None:
    """
    Valida a indexação completa de múltiplos chunks.

    O teste garante que:

    - os chunks são enviados para geração de embeddings;
    - os embeddings são transformados em documentos vetoriais;
    - os documentos são armazenados no VectorStore;
    - a quantidade de documentos indexados é correta;
    - os documentos podem ser recuperados por meio da API pública
      do VectorStore.
    """

    chunks = [
        Chunk(
            id="chunk_1",
            document_name="doc1",
            category="cat1",
            source_path=Path("p1"),
            index=0,
            content="O firewall bloqueou o ataque.",
        ),
        Chunk(
            id="chunk_2",
            document_name="doc2",
            category="cat2",
            source_path=Path("p2"),
            index=0,
            content="Ransomware detectado na rede.",
        ),
    ]

    indexer.index(chunks)

    mock_embedding_generator.generate.assert_called_once_with(
        chunks,
    )

    assert vector_store.size() == 2

    search_results = vector_store.search(
        query_vector=[
            0.1,
            0.2,
            0.3,
            0.4,
        ],
        limit=2,
    )

    assert len(search_results) == 2

    indexed_documents = {
        result.document.id: result.document
        for result in search_results
    }

    for chunk in chunks:
        assert chunk.id in indexed_documents

        document = indexed_documents[chunk.id]

        assert document.id == chunk.id
        assert document.chunk == chunk
        assert document.chunk.content == chunk.content
        assert document.vector == [
            0.1,
            0.2,
            0.3,
            0.4,
        ]


def test_reindexing_replaces_previous_index(
    indexer: KnowledgeIndexer,
    vector_store: InMemoryVectorStore,
) -> None:
    """
    Valida que uma nova indexação reconstrói o índice existente.

    O teste garante que os documentos antigos não permanecem no índice
    após uma nova indexação da Base de Conhecimento.
    """

    initial_chunks = [
        Chunk(
            id="old_chunk",
            document_name="old_document",
            category="old_category",
            source_path=Path("old_path"),
            index=0,
            content="Conteúdo antigo.",
        ),
    ]

    new_chunks = [
        Chunk(
            id="new_chunk_1",
            document_name="new_document",
            category="new_category",
            source_path=Path("new_path"),
            index=0,
            content="Novo conteúdo de segurança.",
        ),
        Chunk(
            id="new_chunk_2",
            document_name="new_document",
            category="new_category",
            source_path=Path("new_path"),
            index=1,
            content="Segundo novo conteúdo de segurança.",
        ),
    ]

    indexer.index(initial_chunks)

    assert vector_store.size() == 1

    indexer.index(new_chunks)

    assert vector_store.size() == 2

    search_results = vector_store.search(
        query_vector=[
            0.1,
            0.2,
            0.3,
            0.4,
        ],
        limit=10,
    )

    result_ids = {
        result.document.id
        for result in search_results
    }

    assert result_ids == {
        "new_chunk_1",
        "new_chunk_2",
    }

    assert "old_chunk" not in result_ids


def test_empty_chunks_do_not_modify_existing_index(
    indexer: KnowledgeIndexer,
    vector_store: InMemoryVectorStore,
    mock_embedding_generator: MagicMock,
) -> None:
    """
    Valida que uma lista vazia de chunks não altera o índice existente.

    O comportamento esperado é preservar os documentos atualmente
    indexados e não executar a geração de embeddings.
    """

    valid_chunk = Chunk(
        id="existing_chunk",
        document_name="document",
        category="category",
        source_path=Path("path"),
        index=0,
        content="Documento existente.",
    )

    indexer.index(
        [
            valid_chunk,
        ],
    )

    mock_embedding_generator.reset_mock()

    indexer.index([])

    assert vector_store.size() == 1

    mock_embedding_generator.generate.assert_not_called()

    search_results = vector_store.search(
        query_vector=[
            0.1,
            0.2,
            0.3,
            0.4,
        ],
        limit=1,
    )

    assert len(search_results) == 1
    assert search_results[0].document.id == "existing_chunk"


def test_embedding_generation_failure_does_not_clear_index(
    indexer: KnowledgeIndexer,
    vector_store: InMemoryVectorStore,
    mock_embedding_generator: MagicMock,
) -> None:
    """
    Valida que uma falha durante a geração dos embeddings não apaga
    o índice anterior.

    Esse comportamento é importante porque o KnowledgeIndexer gera
    os novos embeddings antes de executar clear() no VectorStore.
    """

    valid_chunk = Chunk(
        id="chunk_valid",
        document_name="document",
        category="category",
        source_path=Path("path"),
        index=0,
        content="Log normal.",
    )

    indexer.index(
        [
            valid_chunk,
        ],
    )

    assert vector_store.size() == 1

    mock_embedding_generator.generate.side_effect = ConnectionError(
        "Falha na geração dos embeddings.",
    )

    invalid_chunk = Chunk(
        id="chunk_invalid",
        document_name="document",
        category="category",
        source_path=Path("path"),
        index=0,
        content="Conteúdo que causará falha.",
    )

    with pytest.raises(ConnectionError):
        indexer.index(
            [
                invalid_chunk,
            ],
        )

    assert vector_store.size() == 1

    search_results = vector_store.search(
        query_vector=[
            0.1,
            0.2,
            0.3,
            0.4,
        ],
        limit=1,
    )

    assert len(search_results) == 1
    assert search_results[0].document.id == "chunk_valid"


# ==============================================================================
# TESTES DE RECUPERAÇÃO
# ==============================================================================


def test_semantic_search_success(
    indexer: KnowledgeIndexer,
    retriever: VectorRetriever,
) -> None:
    """
    Valida a recuperação semântica utilizando o VectorStore em memória.

    O teste garante que o VectorRetriever:

    - gera o embedding da consulta;
    - consulta o VectorStore;
    - retorna objetos RetrievedChunk;
    - preserva o Chunk original;
    - fornece score de similaridade;
    - fornece a posição de ranking.
    """

    chunks_to_index = [
        Chunk(
            id="chunk_1",
            document_name="document_1",
            category="authentication",
            source_path=Path("path_1"),
            index=0,
            content="Política de senhas fortes.",
        ),
        Chunk(
            id="chunk_2",
            document_name="document_2",
            category="network_security",
            source_path=Path("path_2"),
            index=0,
            content="Regras de firewall.",
        ),
    ]

    indexer.index(
        chunks_to_index,
    )

    results = retriever.retrieve(
        query="Quais são as políticas de acesso?",
        limit=2,
    )

    assert len(results) == 2

    for position, result in enumerate(
        results,
        start=1,
    ):
        assert isinstance(
            result,
            RetrievedChunk,
        )

        assert isinstance(
            result.chunk,
            Chunk,
        )

        assert isinstance(
            result.score,
            float,
        )

        assert result.rank == position


def test_empty_query_returns_empty_list(
    retriever: VectorRetriever,
) -> None:
    """
    Valida o tratamento de consultas vazias ou compostas apenas
    por espaços em branco.
    """

    results_empty = retriever.retrieve(
        query="",
        limit=5,
    )

    results_spaces = retriever.retrieve(
        query="   ",
        limit=5,
    )

    assert results_empty == []
    assert results_spaces == []


def test_search_respects_limit(
    indexer: KnowledgeIndexer,
    retriever: VectorRetriever,
) -> None:
    """
    Valida que o VectorRetriever respeita o limite máximo de resultados.
    """

    chunks = [
        Chunk(
            id=f"chunk_{index}",
            document_name="security_document",
            category="security",
            source_path=Path("security_path"),
            index=index,
            content=f"Texto de segurança {index}.",
        )
        for index in range(5)
    ]

    indexer.index(chunks)

    results = retriever.retrieve(
        query="Segurança",
        limit=2,
    )

    assert len(results) == 2

    assert results[0].rank == 1
    assert results[1].rank == 2


def test_search_with_limit_one_returns_single_result(
    indexer: KnowledgeIndexer,
    retriever: VectorRetriever,
) -> None:
    """
    Valida a recuperação de apenas um resultado quando limit=1.
    """

    chunks = [
        Chunk(
            id="chunk_1",
            document_name="document",
            category="security",
            source_path=Path("path"),
            index=0,
            content="Primeiro documento de segurança.",
        ),
        Chunk(
            id="chunk_2",
            document_name="document",
            category="security",
            source_path=Path("path"),
            index=1,
            content="Segundo documento de segurança.",
        ),
    ]

    indexer.index(chunks)

    results = retriever.retrieve(
        query="Segurança",
        limit=1,
    )

    assert len(results) == 1
    assert results[0].rank == 1


def test_search_empty_index_returns_empty_list(
    retriever: VectorRetriever,
) -> None:
    """
    Valida que uma busca em um índice vazio retorna uma lista vazia
    sem lançar exceções.
    """

    results = retriever.retrieve(
        query="Threat Intelligence",
        limit=5,
    )

    assert isinstance(
        results,
        list,
    )

    assert results == []


def test_search_with_invalid_limit_raises_value_error(
    retriever: VectorRetriever,
) -> None:
    """
    Valida que um limite de busca inválido é rejeitado pelo VectorStore.

    O VectorRetriever delega a validação do limite para o contrato
    de armazenamento vetorial concreto.
    """

    with pytest.raises(ValueError):
        retriever.retrieve(
            query="Threat Intelligence",
            limit=0,
        )