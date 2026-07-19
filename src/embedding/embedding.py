from __future__ import annotations

from dataclasses import dataclass

from src.chunking.chunk import Chunk


@dataclass(frozen=True, slots=True)
class Embedding:
    """
    Representa um embedding associado a um Chunk.

    O vetor contém a representação numérica do conteúdo
    do Chunk e será utilizado durante a indexação e busca
    vetorial.
    """

    chunk: Chunk

    vector: list[float]