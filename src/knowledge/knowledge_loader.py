from pathlib import Path
from typing import List

from src.config.settings import KNOWLEDGE_DIR
from src.knowledge.knowledge_document import KnowledgeDocument
from src.utils.logger import logger


class KnowledgeLoader:

    def __init__(
        self,
        directory: Path = KNOWLEDGE_DIR
    ):
        self.directory = directory
        self.documents: List[
            KnowledgeDocument
        ] = []


    def load(self):
        self.documents.clear()

        files = self.directory.rglob(
            "*.md"
        )

        for file in files:
            document = self._load_file(
                file
            )
            self.documents.append(
                document
            )

        logger.info(
            "%s documentos carregados.",
            len(self.documents)
        )


    def _load_file(
        self,
        file: Path
    ) -> KnowledgeDocument:
        content = file.read_text(
            encoding="utf-8"
        )

        return KnowledgeDocument(
            name=file.stem,
            category=file.parent.name,
            path=file,
            content=content
        )


    def get_documents(self):
        return self.documents


    def search(
        self,
        query: str,
        limit: int = 5
    ):
        query_terms = (
            query.lower()
            .split()
        )

        scores = []

        for document in self.documents:
            content = (
                document.content
                .lower()
            )

            score = sum(
                term in content
                for term in query_terms
            )

            if score > 0:
                scores.append(
                    (
                        score,
                        document
                    )
                )

        scores.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            document
            for _, document
            in scores[:limit]
        ]