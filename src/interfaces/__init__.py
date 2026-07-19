"""
Contratos e interfaces utilizados pelas diferentes
camadas do CyberSentinel AI.

As interfaces representam pontos de extensão da arquitetura
e permitem manter as implementações concretas desacopladas
das camadas superiores.
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