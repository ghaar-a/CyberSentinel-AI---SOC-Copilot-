from __future__ import annotations

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.interfaces.embedding_provider import EmbeddingProvider


class EmbeddingGenerator:
    """
    Fachada responsável pela geração
    de embeddings.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:

        self.provider = provider

    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:

        return self.provider.generate(
            chunks
        )