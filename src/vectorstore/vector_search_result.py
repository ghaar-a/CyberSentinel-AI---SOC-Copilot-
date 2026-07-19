from __future__ import annotations

from dataclasses import dataclass

from src.vectorstore.vector_document import VectorDocument


@dataclass(frozen=True, slots=True)
class VectorSearchResult:
    """
    Representa o resultado de uma busca vetorial.

    Contém o documento vetorial encontrado e sua pontuação
    de similaridade em relação ao vetor consultado.
    """

    document: VectorDocument

    score: float