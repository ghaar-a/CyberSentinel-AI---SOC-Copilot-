from __future__ import annotations

from abc import ABC, abstractmethod

from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class VectorStore(ABC):
    """
    Contrato responsável pelo armazenamento e recuperação
    de documentos vetoriais.

    Esta abstração desacopla a aplicação de implementações
    específicas como FAISS, ChromaDB, pgvector ou qualquer
    outro mecanismo de armazenamento vetorial.

    O restante da aplicação deve depender apenas deste contrato,
    respeitando o princípio da Inversão de Dependência.
    """

    @abstractmethod
    def add(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Adiciona um documento vetorial ao índice.

        Caso já exista um documento com o mesmo identificador,
        a implementação deverá substituir o documento existente.

        Args:
            document:
                Documento vetorial que será indexado.
        """
        raise NotImplementedError

    @abstractmethod
    def add_many(
        self,
        documents: list[VectorDocument],
    ) -> None:
        """
        Adiciona múltiplos documentos vetoriais ao índice.

        Args:
            documents:
                Lista de documentos que serão indexados.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[VectorSearchResult]:
        """
        Executa uma busca por similaridade vetorial.

        Args:
            query_vector:
                Vetor correspondente à consulta.

            limit:
                Quantidade máxima de resultados retornados.

        Returns:
            Lista contendo os documentos mais similares.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Remove um documento do índice.

        Args:
            document_id:
                Identificador único do documento.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Remove todos os documentos armazenados.
        """
        raise NotImplementedError

    @abstractmethod
    def size(
        self,
    ) -> int:
        """
        Retorna a quantidade de documentos indexados.
        """
        raise NotImplementedError