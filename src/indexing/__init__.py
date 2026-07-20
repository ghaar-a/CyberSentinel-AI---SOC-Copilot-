"""
Pacote responsável pela indexação de conhecimento.

A camada de indexação coordena o processo de transformação
dos embeddings gerados em documentos vetoriais armazenados
em um VectorStore.
"""

from .vector_indexer import VectorIndexer

__all__ = [
    "VectorIndexer",
    "KnowledgeIndexer",
]