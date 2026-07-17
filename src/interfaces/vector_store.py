from abc import ABC, abstractmethod
from typing import List

from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class VectorStore(ABC):
    """
    Contrato para implementações de armazenamento de vetores.

    Esta interface isola a aplicação de tecnologias concretas
    de banco de dados vetorial.

    As implementações podem utilizar:
        - FAISS
        - ChromaDB
        - PostgreSQL + pgvector
        - Milvus
        - Qdrant
        - Armazenamento em memória (In-memory)
    """

    @abstractmethod
    def add(
        self,
        document: VectorDocument
    ) -> None:
        """
        Armazena um documento vetorial.

        Args:
            document:
                Documento contendo metadados de conteúdo
                e o vetor de embedding.
        """
        pass

    @abstractmethod
    def add_many(
        self,
        documents: List[VectorDocument]
    ) -> None:
        """
        Armazena múltiplos documentos vetoriais.

        Args:
            documents:
                Coleção de documentos vetoriais.
        """
        pass

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> List[VectorSearchResult]:
        """
        Realiza busca por similaridade.

        Args:
            query_vector:
                Representação vetorial da consulta.

            top_k:
                Número de resultados retornados.

        Returns:
            Resultados ranqueados da busca vetorial.
        """
        pass

    @abstractmethod
    def delete(
        self,
        document_id: str
    ) -> None:
        """
        Remove um documento do armazenamento.

        Args:
            document_id:
                Identificador do documento armazenado.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Remove todos os vetores armazenados.
        """
        pass