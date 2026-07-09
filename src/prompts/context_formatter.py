# Formata o contexto recuperado da Base de Conhecimento.
from typing import List

from src.knowledge.knowledge_document import KnowledgeDocument


class ContextFormatter:
    """
    Responsável por transformar documentos
    em contexto textual para o LLM.
    """

    def format(
        self,
        documents: List[KnowledgeDocument]
    ) -> str:

        if not documents:
            return (
                "Nenhum documento relevante foi encontrado."
            )

        sections = []

        for document in documents:

            section = (
                f"# Documento\n"
                f"Nome: {document.name}\n"
                f"Categoria: {document.category}\n\n"
                f"{document.content}"
            )

            sections.append(section)

        return "\n\n---\n\n".join(sections)