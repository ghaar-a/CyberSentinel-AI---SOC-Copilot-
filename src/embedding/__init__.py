"""
Componentes relacionados à geração de embeddings.

Este pacote contém as entidades e componentes responsáveis
pela transformação de conteúdo textual em representações vetoriais.
"""

from .embedding import Embedding
from .embedding_generator import EmbeddingGenerator
from .sentence_transformers_embedding_provider import (
    SentenceTransformersEmbeddingProvider,
)

__all__ = [
    "Embedding",
    "EmbeddingGenerator",
    "SentenceTransformersEmbeddingProvider",
]