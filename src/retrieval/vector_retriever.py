from __future__ import annotations

from src.embedding.embedding_generator import EmbeddingGenerator
from src.interfaces.vector_store import VectorStore
from src.retrieval.retrieval_strategy import RetrievalStrategy
from src.retrieval.retrieved_chunk import RetrievedChunk
from src.utils.logger import logger


class VectorRetriever(RetrievalStrategy):
    """
    Estratégia de recuperação baseada em similaridade semântica.

    O VectorRetriever transforma a consulta do usuário em um embedding
    utilizando o EmbeddingGenerator e utiliza esse vetor para pesquisar
    documentos semanticamente semelhantes no VectorStore.

    A classe não conhece a implementação concreta do armazenamento
    vetorial nem do modelo de embeddings.

    Essas responsabilidades são delegadas, respectivamente, para:

    - EmbeddingGenerator;
    - VectorStore.

    Dessa forma, o Retriever permanece desacoplado da infraestrutura
    utilizada pelo sistema.

    O fluxo de recuperação é:

        Pergunta
            ↓
        EmbeddingGenerator
            ↓
        Vetor da consulta
            ↓
        VectorStore
            ↓
        VectorSearchResult
            ↓
        RetrievedChunk
    """

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
    ) -> None:
        """
        Inicializa o recuperador vetorial.

        Args:
            embedding_generator:
                Componente responsável por transformar a consulta
                textual em um embedding.

            vector_store:
                Armazenamento responsável pela busca por similaridade.
        """

        self._embedding_generator = embedding_generator
        self._vector_store = vector_store

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Recupera os chunks semanticamente mais relevantes para uma consulta.

        A consulta é convertida em embedding e enviada ao VectorStore.
        Os resultados retornados são convertidos para RetrievedChunk,
        mantendo o contrato utilizado pelo restante do pipeline RAG.

        Args:
            query:
                Pergunta ou consulta realizada pelo usuário.

            limit:
                Quantidade máxima de chunks retornados.

        Returns:
            Lista de RetrievedChunk ordenada pela relevância retornada
            pelo armazenamento vetorial.

        Raises:
            ValueError:
                Caso a consulta esteja vazia.

            ValueError:
                Caso o limite seja menor ou igual a zero.
        """

        normalized_query = query.strip()

        if not normalized_query:
            raise ValueError(
                "A consulta não pode ser vazia."
            )

        if limit <= 0:
            raise ValueError(
                "O limite da recuperação deve ser maior que zero."
            )

        logger.info(
            "Iniciando recuperação vetorial para a consulta."
        )

        query_chunk = self._create_query_chunk(
            normalized_query,
        )

        query_embedding = self._embedding_generator.generate(
            [query_chunk],
        )[0]

        search_results = self._vector_store.search(
            query_vector=query_embedding.vector,
            limit=limit,
        )

        retrieved_chunks = [
            RetrievedChunk(
                chunk=result.document.chunk,
                score=result.score,
                rank=position + 1,
            )
            for position, result in enumerate(
                search_results,
            )
        ]

        logger.info(
            "Recuperação vetorial concluída. Resultados encontrados: %d",
            len(retrieved_chunks),
        )

        return retrieved_chunks

    @staticmethod
    def _create_query_chunk(
        query: str,
    ):
        """
        Cria um Chunk temporário para representar a consulta.

        O EmbeddingProvider atual trabalha sobre Chunk. Como a consulta
        do usuário não pertence à base de conhecimento, criamos um Chunk
        transitório exclusivamente para gerar o embedding da pergunta.

        O chunk não é armazenado no VectorStore.

        Args:
            query:
                Texto da consulta do usuário.

        Returns:
            Chunk temporário utilizado somente durante a geração
            do embedding da consulta.
        """

        from pathlib import Path

        from src.chunking.chunk import Chunk

        return Chunk(
            id="query",
            document_name="query",
            category="query",
            source_path=Path(""),
            index=0,
            content=query,
        )