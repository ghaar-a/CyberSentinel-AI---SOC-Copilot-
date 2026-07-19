"""
Componentes responsáveis pela recuperação de contexto.

Este pacote contém as abstrações e estratégias utilizadas
para recuperar informações relevantes da base de conhecimento.
"""

from .keyword_chunk_retriever import KeywordChunkRetriever
from .retrieval_strategy import RetrievalStrategy
from .retrieved_chunk import RetrievedChunk
from .retriever import Retriever
from .vector_retriever import VectorRetriever

__all__ = [
    "KeywordChunkRetriever",
    "RetrievalStrategy",
    "RetrievedChunk",
    "Retriever",
    "VectorRetriever",
]