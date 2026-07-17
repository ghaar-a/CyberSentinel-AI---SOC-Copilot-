from __future__ import annotations

from dataclasses import dataclass

from src.vectorstore.vector_document import VectorDocument


@dataclass(slots=True, frozen=True)
class VectorSearchResult:
    """
    Representa o resultado de uma busca vetorial.

    Esta entidade encapsula um documento recuperado e sua
    pontuação de similaridade.

    Ela pertence exclusivamente à camada de armazenamento
    vetorial e será posteriormente convertida para
    RetrievedChunk pelo VectorRetriever.

    Dessa forma, o restante da aplicação permanece
    desacoplado da tecnologia utilizada para busca vetorial.
    """

    document: VectorDocument

    score: float