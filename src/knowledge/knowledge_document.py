from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnowledgeDocument:

    name: str

    category: str

    path: Path

    content: str