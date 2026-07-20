"""
Componentes relacionados ao armazenamento vetorial.

Este pacote contém as entidades e implementações concretas
utilizadas pelo pipeline de recuperação semântica.

Os contratos arquiteturais permanecem definidos na camada
src.interfaces.
"""

from .chroma_vector_store import ChromaVectorStore
from .in_memory_vector_store import InMemoryVectorStore
from .vector_document import VectorDocument
from .vector_search_result import VectorSearchResult

__all__ = [
    "ChromaVectorStore",
    "InMemoryVectorStore",
    "VectorDocument",
    "VectorSearchResult",
]