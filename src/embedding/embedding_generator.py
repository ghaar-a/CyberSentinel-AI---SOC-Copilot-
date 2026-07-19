from __future__ import annotations

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.interfaces.embedding_provider import EmbeddingProvider


class EmbeddingGenerator:
    """
    Fachada responsável pela geração de embeddings.

    Esta classe coordena a utilização de um EmbeddingProvider,
    mantendo a aplicação desacoplada da tecnologia utilizada
    para geração dos vetores.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:
        """
        Inicializa o gerador de embeddings.

        Args:
            provider:
                Implementação responsável pela geração
                dos embeddings.
        """

        self._provider = provider

    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        """
        Gera embeddings para os chunks informados.

        Args:
            chunks:
                Chunks que serão transformados em embeddings.

        Returns:
            Lista de embeddings gerados.
        """

        return self._provider.generate(
            chunks,
        )

    def generate_query_embedding(
        self,
        query: str,
    ) -> list[float]:
        """
        Gera um embedding para uma consulta textual.

        Args:
            query:
                Consulta realizada pelo usuário.

        Returns:
            Vetor correspondente à consulta.
        """

        return self._provider.generate_query_embedding(
            query,
        )