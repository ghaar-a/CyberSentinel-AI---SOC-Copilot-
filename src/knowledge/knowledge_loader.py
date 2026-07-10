# Responsável pela base de conhecimento
from pathlib import Path
from typing import List

from src.config.settings import KNOWLEDGE_DIR
from src.interfaces.knowledge_provider import KnowledgeProvider
from src.knowledge.knowledge_document import KnowledgeDocument
from src.utils.logger import logger


class KnowledgeLoader(KnowledgeProvider):
    """
    Responsável por carregar e consultar a Base de Conhecimento.
    """

    def __init__(self, knowledge_directory: Path = KNOWLEDGE_DIR):
        self.knowledge_directory = knowledge_directory
        self._documents: List[KnowledgeDocument] = []

    @property
    def documents(self) -> List[KnowledgeDocument]:
        """
        Retorna uma cópia da coleção de documentos carregados.
        """
        return list(self._documents)

    def load(self) -> None:
        """
        Carrega todos os arquivos Markdown da Base de Conhecimento.
        """

        self._documents.clear()

        if not self.knowledge_directory.exists():
            raise FileNotFoundError(
                f"Diretório não encontrado: {self.knowledge_directory}"
            )

        markdown_files = sorted(
            self.knowledge_directory.rglob("*.md")
        )

        logger.info(
            "Carregando %s documentos...",
            len(markdown_files)
        )

        for file_path in markdown_files:
            document = self._load_document(file_path)
            self._documents.append(document)

        logger.info(
            "Base de Conhecimento carregada com sucesso."
        )

    def search(
        self,
        query: str,
        limit: int = 5
    ) -> List[KnowledgeDocument]:
        """
        Busca simples baseada em palavras-chave.

        Esta implementação será substituída futuramente
        por um mecanismo RAG utilizando embeddings.
        """

        terms = {
            term.lower()
            for term in query.split()
        }

        ranking = []

        for document in self._documents:

            text = (
                f"{document.name}\n"
                f"{document.category}\n"
                f"{document.content}"
            ).lower()

            score = sum(
                term in text
                for term in terms
            )

            if score > 0:
                ranking.append(
                    (
                        score,
                        document
                    )
                )

        ranking.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            document
            for _, document
            in ranking[:limit]
        ]

    def statistics(self) -> dict:

        categories = {}

        for document in self._documents:
            categories.setdefault(
                document.category,
                0
            )

            categories[
                document.category
            ] += 1

        return {
            "documents": len(self._documents),
            "categories": categories
        }

    def _load_document(
        self,
        file_path: Path
    ) -> KnowledgeDocument:

        content = file_path.read_text(
            encoding="utf-8"
        )

        return KnowledgeDocument(
            name=file_path.stem,
            category=file_path.parent.name,
            path=file_path,
            content=content
        )