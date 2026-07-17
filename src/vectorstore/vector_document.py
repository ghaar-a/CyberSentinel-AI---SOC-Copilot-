from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class VectorDocument:
    """
    Representa um documento preparado para indexação vetorial.

    Esta entidade é independente da origem do conteúdo.

    Um VectorDocument representa exatamente aquilo que será
    armazenado em um banco vetorial.

    Diferentemente de Chunk, esta entidade não possui
    responsabilidades relacionadas ao processo de divisão
    de documentos.

    Ela representa apenas:

    - conteúdo textual;
    - vetor correspondente;
    - metadados necessários para recuperação.
    """

    id: str

    document_name: str

    category: str

    source_path: Path

    chunk_index: int

    content: str

    embedding: list[float]