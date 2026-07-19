"""
Componentes relacionados ao armazenamento vetorial.

Este pacote contém as entidades e implementações concretas
utilizadas para indexação e recuperação de documentos vetoriais.

Os contratos das implementações são definidos na camada
src.interfaces.
"""

from .in_memory_vector_store import InMemoryVectorStore
from .vector_document import VectorDocument
from .vector_search_result import VectorSearchResult

__all__ = [
    "InMemoryVectorStore",
    "VectorDocument",
    "VectorSearchResult",
]