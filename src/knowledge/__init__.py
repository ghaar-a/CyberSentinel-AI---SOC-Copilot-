"""
Pacote responsável pela Base de Conhecimento
do CyberSentinel AI.

Esta camada possui apenas a responsabilidade
de carregar e representar documentos utilizados
pela aplicação.
"""

from .knowledge_document import KnowledgeDocument
from .knowledge_loader import KnowledgeLoader

__all__ = [
    "KnowledgeDocument",
    "KnowledgeLoader",
]