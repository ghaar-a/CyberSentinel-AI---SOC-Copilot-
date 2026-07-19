from __future__ import annotations

from dataclasses import dataclass

from src.chunking.chunk import Chunk


@dataclass(frozen=True, slots=True)
class VectorDocument:
    """
    Representa um documento vetorial indexável.

    Um VectorDocument associa um Chunk ao seu vetor
    de embedding correspondente.

    O Chunk mantém o conteúdo original e os metadados
    necessários para reconstrução do contexto.

    O vetor representa semanticamente o conteúdo do Chunk
    e será utilizado pelo mecanismo de busca vetorial.
    """

    id: str

    chunk: Chunk

    vector: list[float]