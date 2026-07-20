from __future__ import annotations

from src.embedding.embedding_generator import EmbeddingGenerator
from src.interfaces.vector_store import VectorStore
from src.retrieval.retrieval_strategy import RetrievalStrategy
from src.retrieval.retrieved_chunk import RetrievedChunk


class VectorRetriever(RetrievalStrategy):
    """
    Estratégia de recuperação baseada em similaridade semântica.

    O fluxo de recuperação é:

    1. Receber a pergunta do usuário.
    2. Gerar o embedding da consulta.
    3. Consultar o VectorStore.
    4. Converter os resultados vetoriais em RetrievedChunk.

    A classe não conhece a implementação concreta do modelo
    de embeddings nem do armazenamento vetorial.
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
                em uma representação vetorial.

            vector_store:
                Contrato responsável pela busca de similaridade.
        """

        self._embedding_generator = embedding_generator
        self._vector_store = vector_store

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Recupera os chunks semanticamente mais relevantes.

        Args:
            query:
                Pergunta ou consulta realizada pelo usuário.

            limit:
                Quantidade máxima de resultados retornados.

        Returns:
            Lista de RetrievedChunk ordenada por relevância.
        """

        if not query or not query.strip():
            return []

        query_chunk = self._create_query_chunk(
            query=query,
        )

        query_embedding = self._embedding_generator.generate(
            [query_chunk],
        )[0]

        search_results = self._vector_store.search(
            query_vector=query_embedding.vector,
            limit=limit,
        )

        return [
            RetrievedChunk(
                chunk=result.document.chunk,
                score=result.score,
                rank=position + 1,
            )
            for position, result in enumerate(search_results)
        ]

    @staticmethod
    def _create_query_chunk(
        query: str,
    ):
        """
        Cria um Chunk temporário para representar a consulta.

        O chunk é utilizado apenas como entrada para o contrato
        existente de geração de embeddings.

        A consulta não é persistida no VectorStore.
        """

        from pathlib import Path

        from src.chunking.chunk import Chunk

        return Chunk(
            id="query",
            document_name="query",
            category="query",
            source_path=Path("."),
            index=0,
            content=query.strip(),
        )