from __future__ import annotations

from dataclasses import dataclass

from src.chunking.chunk import Chunk


@dataclass(slots=True)
class Embedding:
    """
    Representa um embedding associado
    a um Chunk.

    Esta entidade será utilizada pelos
    bancos vetoriais.
    """

    chunk: Chunk

    vector: list[float]