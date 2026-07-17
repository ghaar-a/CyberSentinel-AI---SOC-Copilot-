"""
Pacote responsável pela camada de recuperação
(Retrieval) do CyberSentinel AI.

Esta camada abstrai completamente a estratégia
utilizada para localizar informações relevantes.

Atualmente a aplicação utiliza recuperação por
palavras-chave, mas a arquitetura foi preparada
para evolução para recuperação vetorial (RAG)
sem alterações nas camadas superiores.
"""

from .keyword_chunk_retriever import KeywordChunkRetriever
from .retrieved_chunk import RetrievedChunk
from .retrieval_strategy import RetrievalStrategy
from .retriever import Retriever

__all__ = [
    "KeywordChunkRetriever",
    "RetrievedChunk",
    "RetrievalStrategy",
    "Retriever",
]