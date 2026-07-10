from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Chunk:
    """
    Representa um fragmento de um documento.

    Esta entidade será utilizada futuramente
    para armazenar embeddings e metadados.
    """

    id: str

    document_name: str

    category: str

    source_path: Path

    index: int

    content: str