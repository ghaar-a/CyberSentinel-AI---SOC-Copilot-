"""
Pacote responsável pela geração de embeddings.

Esta camada abstrai completamente a tecnologia utilizada
para transformar texto em vetores.

Implementações futuras poderão utilizar:

- Sentence Transformers
- Google Gemini Embeddings
- OpenAI Embeddings
- Cohere Embeddings

sem alterar o restante da aplicação.
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