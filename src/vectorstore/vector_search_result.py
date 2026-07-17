from dataclasses import dataclass
from src.vectorstore.vector_document import VectorDocument


@dataclass(frozen=True)
class VectorSearchResult:
    """
    Representa o resultado de uma busca por similaridade.

    Contém:
        - o documento correspondente
        - a pontuação de similaridade (score)
    """

    document: VectorDocument

    score: float