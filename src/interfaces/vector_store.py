from __future__ import annotations

from abc import ABC, abstractmethod

from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class VectorStore(ABC):
    """
    Contrato para armazenamento e recuperação de documentos vetoriais.

    A interface desacopla a aplicação da tecnologia concreta utilizada
    para indexação e busca vetorial.

    Implementações possíveis incluem:

    - Armazenamento em memória para testes.
    - ChromaDB para armazenamento vetorial persistente.
    - FAISS para busca vetorial de alto desempenho.
    - pgvector para integração com PostgreSQL.

    As camadas superiores da aplicação dependem somente deste contrato,
    respeitando o princípio da Inversão de Dependência.
    """

    @abstractmethod
    def add(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Adiciona ou atualiza um documento vetorial.

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
        Adiciona ou atualiza múltiplos documentos vetoriais.

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
                Quantidade máxima de resultados.

        Returns:
            Lista de resultados ordenados por relevância.
        """

        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Remove um documento vetorial.

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