from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True)
class Embedding:
    """
    Representa a representação vetorial
    gerada a partir de um conteúdo.

    Um embedding é uma estrutura matemática
    utilizada para busca semântica.

    Ele não conhece a origem do conteúdo,
    apenas mantém o vetor e seus metadados.
    """

    id: str

    vector: list[float]

    metadata: Dict[str, str]