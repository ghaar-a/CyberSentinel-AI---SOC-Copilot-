from __future__ import annotations

from src.embedding.embedding_generator import EmbeddingGenerator
from src.interfaces.vector_store import VectorStore
from src.retrieval.retrieval_strategy import RetrievalStrategy
from src.retrieval.retrieved_chunk import RetrievedChunk


class VectorRetriever(
    RetrievalStrategy,
):
    """
    Estratégia de recuperação baseada em similaridade vetorial.

    Responsável por transformar a consulta do usuário em um embedding,
    executar a busca no VectorStore e converter os resultados vetoriais
    para RetrievedChunk.

    Dessa forma, as camadas superiores continuam desacopladas da
    tecnologia utilizada para armazenamento e recuperação vetorial.
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
                Componente responsável por gerar embeddings.

            vector_store:
                Armazenamento vetorial utilizado para realizar
                a busca por similaridade.
        """

        self._embedding_generator = (
            embedding_generator
        )

        self._vector_store = (
            vector_store
        )

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Recupera os chunks semanticamente mais relevantes
        para a consulta informada.

        Args:
            query:
                Pergunta ou consulta realizada pelo usuário.

            limit:
                Quantidade máxima de chunks retornados.

        Returns:
            Lista de RetrievedChunk ordenada por relevância.
        """

        if not query.strip():
            return []

        if limit <= 0:
            return []

        query_vector = (
            self._embedding_generator.generate_query_embedding(
                query,
            )
        )

        if not query_vector:
            return []

        search_results = (
            self._vector_store.search(
                query_vector=query_vector,
                limit=limit,
            )
        )

        return [
            RetrievedChunk(
                chunk=result.document.chunk,
                score=result.score,
                rank=position + 1,
            )
            for position, result in enumerate(
                search_results,
            )
        ]