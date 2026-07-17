"""
Pacote responsável pelo armazenamento vetorial da aplicação.

Esta camada abstrai completamente a tecnologia utilizada para
armazenamento e recuperação vetorial.

Implementações futuras poderão utilizar:

- InMemory
- FAISS
- ChromaDB
- pgvector
- Milvus
- Qdrant

sem alterar o restante da aplicação.
"""

from .in_memory_vector_store import InMemoryVectorStore
from .vector_document import VectorDocument
from .vector_indexer import VectorIndexer
from .vector_search_result import VectorSearchResult

__all__ = [
    "InMemoryVectorStore",
    "VectorDocument",
    "VectorIndexer",
    "VectorSearchResult",
]