"""
Pacote responsável pelo agente principal do CyberSentinel AI.

O agente orquestra o fluxo da aplicação,
coordenando recuperação de contexto,
construção do prompt e comunicação
com o modelo de linguagem.
"""

from .cyber_sentinel_agent import CyberSentinelAgent

__all__ = [
    "CyberSentinelAgent",
]