"""
Pacote responsável pelas implementações de Large Language Models (LLMs).

Novas implementações poderão ser adicionadas futuramente sem alterar
o restante da aplicação, desde que implementem a interface LLMProvider.

Exemplos:
- GeminiClient
- OpenAIClient
- ClaudeClient
- OllamaClient
"""

from .gemini_client import GeminiClient

__all__ = [
    "GeminiClient",
]