# Carrega e mantém os arquivos Markdown em cache.
from pathlib import Path
from typing import Dict

from src.utils.logger import logger


class PromptLoader:
    """
    Responsável por carregar e manter em cache
    todos os arquivos de prompt.
    """

    def __init__(self, prompts_directory: Path):
        self.prompts_directory = prompts_directory
        self._cache: Dict[str, str] = {}

    def load(self, filename: str) -> str:
        """
        Retorna o conteúdo de um arquivo Markdown.

        Caso o arquivo já tenha sido carregado,
        retorna o conteúdo do cache.
        """

        if filename in self._cache:
            return self._cache[filename]

        file_path = self.prompts_directory / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Prompt não encontrado: {file_path}"
            )

        content = file_path.read_text(
            encoding="utf-8"
        )

        self._cache[filename] = content

        logger.info(
            "Prompt carregado: %s",
            filename
        )

        return content

    def clear_cache(self) -> None:
        """
        Limpa o cache de prompts.
        """

        self._cache.clear()

        logger.info(
            "Cache de prompts limpo."
        )