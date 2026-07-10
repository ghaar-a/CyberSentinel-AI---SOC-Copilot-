from pathlib import Path

from src.config.settings import KNOWLEDGE_DIR
from src.interfaces.document_repository import DocumentRepository
from src.knowledge.knowledge_document import KnowledgeDocument
from src.utils.logger import logger


class KnowledgeLoader(DocumentRepository):
    """
    Responsável apenas por carregar documentos
    da Base de Conhecimento.

    Não possui qualquer lógica de recuperação.
    """

    def __init__(
        self,
        knowledge_directory: Path = KNOWLEDGE_DIR
    ) -> None:

        self.knowledge_directory = knowledge_directory
        self._documents: list[KnowledgeDocument] = []

    @property
    def documents(
        self,
    ) -> list[KnowledgeDocument]:

        return list(self._documents)

    def get_all(
        self,
    ) -> list[KnowledgeDocument]:

        return self.documents

    def load(
        self,
    ) -> None:

        self._documents.clear()

        if not self.knowledge_directory.exists():
            raise FileNotFoundError(
                f"Diretório inexistente: {self.knowledge_directory}"
            )

        markdown_files = sorted(
            self.knowledge_directory.rglob("*.md")
        )

        logger.info(
            "Carregando %d documentos...",
            len(markdown_files)
        )

        for file_path in markdown_files:

            document = self._load_document(
                file_path
            )

            self._documents.append(
                document
            )

        logger.info(
            "Base carregada com sucesso."
        )

    def statistics(
        self,
    ) -> dict:

        categories: dict[str, int] = {}

        for document in self._documents:

            categories.setdefault(
                document.category,
                0
            )

            categories[
                document.category
            ] += 1

        return {
            "documents": len(
                self._documents
            ),
            "categories": categories,
        }

    def _load_document(
        self,
        file_path: Path
    ) -> KnowledgeDocument:

        return KnowledgeDocument(
            name=file_path.stem,
            category=file_path.parent.name,
            path=file_path,
            content=file_path.read_text(
                encoding="utf-8"
            ),
        )