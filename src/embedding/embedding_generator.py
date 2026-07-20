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

    A fachada permite que o restante da aplicação trabalhe com
    uma única entrada para geração de embeddings, independentemente
    do provedor concreto utilizado.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:
        """
        Inicializa o gerador de embeddings.

        Args:
            provider:
                Implementação responsável pela geração dos embeddings.
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