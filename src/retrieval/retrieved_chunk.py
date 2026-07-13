from __future__ import annotations

from dataclasses import dataclass

from src.chunking.chunk import Chunk


@dataclass(slots=True)
class RetrievedChunk:
    """
    Representa um chunk recuperado
    juntamente com seus metadados
    de recuperação.

    Esta entidade será utilizada
    tanto pela busca por palavras-chave
    quanto pela busca vetorial.
    """

    chunk: Chunk

    score: float

    rank: int