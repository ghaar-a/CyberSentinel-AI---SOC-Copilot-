from __future__ import annotations

from src.retrieval.retrieved_chunk import RetrievedChunk


class ContextFormatter:
    """
    Formata os chunks recuperados
    para construção do prompt.
    """

    def format(
        self,
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:

        if not retrieved_chunks:

            return (
                "Nenhum contexto relevante encontrado."
            )

        sections = []

        for item in retrieved_chunks:

            chunk = item.chunk

            sections.append(
                f"""
Documento: {chunk.document_name}

Categoria: {chunk.category}

Relevância: {item.score:.2f}

Trecho:

{chunk.content}
""".strip()
            )

        return "\n\n----------------------\n\n".join(
            sections
        )