from __future__ import annotations

import math

from src.interfaces.vector_store import VectorStore
from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class InMemoryVectorStore(VectorStore):
    """
    Implementação simples de um banco vetorial em memória.

    Esta implementação possui dois objetivos principais:

    1. Validar toda a arquitetura antes da integração com
       FAISS ou outro banco vetorial.

    2. Permitir testes unitários sem dependência de
       bibliotecas externas.

    Os documentos são armazenados em memória utilizando
    um dicionário indexado pelo identificador.
    """

    def __init__(self) -> None:
        """
        Inicializa o armazenamento interno.
        """

        self._documents: dict[str, VectorDocument] = {}

    def add(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Adiciona um documento ao armazenamento.

        Caso o identificador já exista, o documento será
        substituído.

        Args:
            document:
                Documento vetorial.
        """

        self._documents[document.id] = document

    def add_many(
        self,
        documents: list[VectorDocument],
    ) -> None:
        """
        Adiciona múltiplos documentos.

        Args:
            documents:
                Lista de documentos vetoriais.
        """

        for document in documents:
            self.add(document)

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[VectorSearchResult]:
        """
        Executa busca utilizando similaridade do cosseno.

        Args:
            query_vector:
                Vetor representando a consulta.

            limit:
                Quantidade máxima de resultados.

        Returns:
            Lista ordenada dos documentos mais similares.
        """

        results: list[VectorSearchResult] = []

        for document in self._documents.values():

            similarity = self._cosine_similarity(
                query_vector,
                document.embedding,
            )

            results.append(
                VectorSearchResult(
                    document=document,
                    score=similarity,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:limit]

    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Remove um documento.

        Args:
            document_id:
                Identificador do documento.
        """

        self._documents.pop(
            document_id,
            None,
        )

    def clear(self) -> None:
        """
        Remove todos os documentos armazenados.
        """

        self._documents.clear()

    def size(self) -> int:
        """
        Retorna a quantidade de documentos armazenados.
        """

        return len(self._documents)

    @staticmethod
    def _cosine_similarity(
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        """
        Calcula a similaridade do cosseno entre dois vetores.

        Quanto mais próximo de 1, maior a similaridade.

        Args:
            vector_a:
                Primeiro vetor.

            vector_b:
                Segundo vetor.

        Returns:
            Valor da similaridade.
        """

        if len(vector_a) != len(vector_b):
            raise ValueError(
                "Os vetores devem possuir a mesma dimensão."
            )

        produto_escalar = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        norma_a = math.sqrt(
            sum(
                valor * valor
                for valor in vector_a
            )
        )

        norma_b = math.sqrt(
            sum(
                valor * valor
                for valor in vector_b
            )
        )

        if norma_a == 0 or norma_b == 0:
            return 0.0

        return produto_escalar / (norma_a * norma_b)