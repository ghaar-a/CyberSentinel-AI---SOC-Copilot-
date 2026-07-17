"""
Pacote responsável pelas configurações globais
da aplicação.

Todas as configurações são centralizadas
em Settings e carregadas por meio do
Pydantic Settings.
"""

from .settings import settings

__all__ = [
    "settings",
]