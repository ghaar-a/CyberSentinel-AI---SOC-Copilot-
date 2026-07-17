"""
Pacote responsável pela Prompt Engine do CyberSentinel AI.

A construção do prompt foi dividida em componentes
especializados para manter alta coesão e baixo acoplamento.
"""

from .context_formatter import ContextFormatter
from .prompt_builder import PromptBuilder
from .prompt_loader import PromptLoader
from .prompt_manager import PromptManager

__all__ = [
    "ContextFormatter",
    "PromptBuilder",
    "PromptLoader",
    "PromptManager",
]