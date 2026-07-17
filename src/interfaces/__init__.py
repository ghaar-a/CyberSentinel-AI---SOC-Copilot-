"""
Pacote que reúne todos os contratos (interfaces) da aplicação.

As interfaces definem os pontos de extensão da arquitetura,
permitindo que implementações concretas sejam substituídas
sem impactar as demais camadas.
"""

from .chunk_provider import ChunkProvider
from .document_repository import DocumentRepository
from .embedding_provider import EmbeddingProvider
from .llm_provider import LLMProvider
from .prompt_provider import PromptProvider
from .vector_store import VectorStore

__all__ = [
    "ChunkProvider",
    "DocumentRepository",
    "EmbeddingProvider",
    "LLMProvider",
    "PromptProvider",
    "VectorStore",
]