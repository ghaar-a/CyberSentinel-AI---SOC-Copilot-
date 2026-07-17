from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class VectorDocument:
    """
    Representa um documento armazenado em um banco de dados vetorial.

    Um VectorDocument é a ponte entre:
        - Fragmentos de conhecimento (chunks)
        - Geração de embeddings
        - Armazenamento vetorial
    """

    id: str

    content: str

    embedding: List[float]

    metadata: Dict[str, str]