from __future__ import annotations

from uuid import uuid4

from src.chunking.chunk import Chunk
from src.chunking.chunker import Chunker
from src.interfaces.chunk_provider import ChunkProvider
from src.interfaces.document_repository import DocumentRepository


class MarkdownChunker(
    Chunker,
    ChunkProvider,
):
    """
    Divide documentos Markdown em chunks.

    Nesta primeira versão cada seção
    iniciada por '#' gera um chunk.

    No futuro evoluiremos para um
    Recursive Text Splitter.
    """

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:

        self.repository = repository

        self._chunks: list[Chunk] = []

    def chunk(self) -> list[Chunk]:

        self._chunks.clear()

        for document in self.repository.get_all():

            sections = []

            current = []

            for line in document.content.splitlines():

                if line.startswith("#") and current:

                    sections.append(
                        "\n".join(current)
                    )

                    current = []

                current.append(line)

            if current:
                sections.append(
                    "\n".join(current)
                )

            for index, section in enumerate(sections):

                self._chunks.append(
                    Chunk(
                        id=str(uuid4()),
                        document_name=document.name,
                        category=document.category,
                        source_path=document.path,
                        index=index,
                        content=section.strip(),
                    )
                )

        return self._chunks

    def get_chunks(self) -> list[Chunk]:

        if not self._chunks:
            self.chunk()

        return list(self._chunks)