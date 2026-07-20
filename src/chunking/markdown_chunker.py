from __future__ import annotations

import hashlib

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

    Cada seção iniciada por um título Markdown é tratada
    como um chunk independente.

    O identificador do chunk é determinístico. Isso permite
    que o mesmo conteúdo gere sempre o mesmo ID, evitando
    duplicações durante processos de reindexação.

    Esta implementação mantém a arquitetura preparada para
    futuras estratégias de divisão de texto, como Recursive
    Character Text Splitter.
    """

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:
        """
        Inicializa o chunker.

        Args:
            repository:
                Repositório responsável por fornecer os documentos
                da base de conhecimento.
        """

        self._repository = repository
        self._chunks: list[Chunk] = []

    def chunk(self) -> list[Chunk]:
        """
        Divide todos os documentos disponíveis em chunks.

        O processo é determinístico. Um mesmo documento,
        com o mesmo conteúdo e na mesma posição, produzirá
        sempre o mesmo identificador.

        Returns:
            Lista completa de chunks gerados.
        """

        self._chunks.clear()

        for document in self._repository.get_all():
            sections: list[str] = []
            current_section: list[str] = []

            for line in document.content.splitlines():

                if line.startswith("#") and current_section:
                    sections.append(
                        "\n".join(current_section)
                    )

                    current_section = []

                current_section.append(line)

            if current_section:
                sections.append(
                    "\n".join(current_section)
                )

            for index, section in enumerate(sections):

                content = section.strip()

                if not content:
                    continue

                chunk_id = self._generate_chunk_id(
                    document_path=str(document.path),
                    index=index,
                    content=content,
                )

                self._chunks.append(
                    Chunk(
                        id=chunk_id,
                        document_name=document.name,
                        category=document.category,
                        source_path=document.path,
                        index=index,
                        content=content,
                    )
                )

        return list(self._chunks)

    def get_chunks(self) -> list[Chunk]:
        """
        Retorna os chunks atualmente disponíveis.

        Caso os chunks ainda não tenham sido gerados,
        executa automaticamente o processo de chunking.

        Returns:
            Lista de chunks disponíveis.
        """

        if not self._chunks:
            self.chunk()

        return list(self._chunks)

    @staticmethod
    def _generate_chunk_id(
        document_path: str,
        index: int,
        content: str,
    ) -> str:
        """
        Gera um identificador determinístico para um chunk.

        O ID é baseado no caminho do documento, posição do chunk
        e conteúdo. Dessa forma, o mesmo conteúdo produz sempre
        o mesmo identificador.

        Args:
            document_path:
                Caminho do documento original.

            index:
                Índice do chunk dentro do documento.

            content:
                Conteúdo textual do chunk.

        Returns:
            Identificador hexadecimal baseado em SHA-256.
        """

        raw_identifier = (
            f"{document_path}|"
            f"{index}|"
            f"{content}"
        )

        return hashlib.sha256(
            raw_identifier.encode("utf-8")
        ).hexdigest()