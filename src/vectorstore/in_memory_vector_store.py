from __future__ import annotations

import math

from src.interfaces.vector_store import VectorStore
from src.utils.logger import logger
from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class InMemoryVectorStore(VectorStore):
    """
    Implementação de VectorStore baseada em memória.

    Esta implementação é utilizada como uma primeira infraestrutura
    concreta para validar o pipeline de recuperação vetorial.

    Os documentos são mantidos apenas durante a execução da aplicação.
    Ao reiniciar o processo, o índice é perdido.

    A implementação utiliza similaridade de cosseno para comparar
    o vetor da consulta com os vetores armazenados.

    Esta classe não deve ser confundida com a implementação definitiva
    de produção. Seu principal objetivo é validar o contrato VectorStore
    e permitir testes rápidos da arquitetura antes da adoção de uma
    solução persistente como ChromaDB ou pgvector.
    """

    def __init__(self) -> None:
        """
        Inicializa um armazenamento vetorial vazio.
        """

        self._documents: dict[
            str,
            VectorDocument,
        ] = {}

    def add(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Adiciona ou substitui um documento vetorial.

        O identificador do VectorDocument é utilizado como chave
        única do armazenamento.

        Args:
            document:
                Documento vetorial que será armazenado.
        """

        self._documents[
            document.id
        ] = document

    def add_many(
        self,
        documents: list[VectorDocument],
    ) -> None:
        """
        Adiciona ou substitui múltiplos documentos vetoriais.

        Args:
            documents:
                Lista de documentos vetoriais que serão armazenados.
        """

        for document in documents:
            self.add(
                document,
            )

        logger.info(
            "Documentos vetoriais indexados: %d",
            len(documents),
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[VectorSearchResult]:
        """
        Executa uma busca por similaridade de cosseno.

        Args:
            query_vector:
                Vetor correspondente à consulta do usuário.

            limit:
                Quantidade máxima de resultados retornados.

        Returns:
            Lista de resultados ordenados da maior para a menor
            similaridade.

        Raises:
            ValueError:
                Caso o vetor da consulta esteja vazio.
            ValueError:
                Caso o limite seja menor ou igual a zero.
        """

        if not query_vector:
            raise ValueError(
                "O vetor da consulta não pode estar vazio."
            )

        if limit <= 0:
            raise ValueError(
                "O limite da busca deve ser maior que zero."
            )

        if not self._documents:
            return []

        results: list[VectorSearchResult] = []

        for document in self._documents.values():

            score = self._cosine_similarity(
                query_vector,
                document.vector,
            )

            results.append(
                VectorSearchResult(
                    document=document,
                    score=score,
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
        Remove um documento vetorial do armazenamento.

        Caso o identificador não exista, nenhuma exceção é lançada.

        Args:
            document_id:
                Identificador do documento que será removido.
        """

        self._documents.pop(
            document_id,
            None,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove todos os documentos do armazenamento.
        """

        self._documents.clear()

    def size(
        self,
    ) -> int:
        """
        Retorna a quantidade de documentos indexados.
        """

        return len(
            self._documents,
        )

    @staticmethod
    def _cosine_similarity(
        first_vector: list[float],
        second_vector: list[float],
    ) -> float:
        """
        Calcula a similaridade de cosseno entre dois vetores.

        Como os embeddings produzidos pelo provider são normalizados,
        o cálculo poderia ser simplificado para um produto escalar.
        A implementação mantém a fórmula explícita para tornar a
        responsabilidade do armazenamento mais clara e independente
        da implementação do provider.

        Args:
            first_vector:
                Primeiro vetor.

            second_vector:
                Segundo vetor.

        Returns:
            Valor de similaridade entre -1.0 e 1.0.

        Raises:
            ValueError:
                Caso os vetores possuam dimensões diferentes.
        """

        if len(first_vector) != len(second_vector):
            raise ValueError(
                "Os vetores devem possuir a mesma dimensão."
            )

        first_norm = math.sqrt(
            sum(
                value * value
                for value in first_vector
            )
        )

        second_norm = math.sqrt(
            sum(
                value * value
                for value in second_vector
            )
        )

        if first_norm == 0.0 or second_norm == 0.0:
            return 0.0

        dot_product = sum(
            first_value * second_value
            for first_value, second_value in zip(
                first_vector,
                second_vector,
                strict=True,
            )
        )

        return dot_product / (
            first_norm * second_norm
        )