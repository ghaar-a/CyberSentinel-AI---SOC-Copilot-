from __future__ import annotations

import math

from src.interfaces.vector_store import VectorStore
from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class InMemoryVectorStore(VectorStore):
    """
    Implementação de VectorStore baseada em memória.

    Esta implementação será utilizada inicialmente para validar
    o pipeline de RAG sem introduzir imediatamente uma dependência
    de infraestrutura como FAISS ou ChromaDB.

    Os documentos são mantidos em memória e a busca utiliza
    similaridade de cosseno.

    Esta implementação não possui persistência. Portanto,
    todos os dados são perdidos quando a aplicação é encerrada.

    Em uma etapa posterior, poderá ser substituída por uma
    implementação baseada em FAISS ou outro mecanismo vetorial
    sem alterar o contrato utilizado pelas camadas superiores.
    """

    def __init__(self) -> None:
        """
        Inicializa o armazenamento vetorial em memória.
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
        Adiciona um documento ao armazenamento.

        Caso já exista um documento com o mesmo identificador,
        o documento existente será substituído.

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
        Adiciona múltiplos documentos ao armazenamento.

        Caso algum documento possua um identificador já existente,
        o documento anterior será substituído.

        Args:
            documents:
                Documentos vetoriais que serão armazenados.
        """

        for document in documents:
            self.add(
                document,
            )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[VectorSearchResult]:
        """
        Busca os documentos mais similares ao vetor informado.

        A similaridade utilizada é a similaridade de cosseno.

        Args:
            query_vector:
                Vetor utilizado como consulta.

            limit:
                Quantidade máxima de resultados retornados.

        Returns:
            Lista de resultados ordenados da maior para a menor
            similaridade.
        """

        if not query_vector:
            return []

        if limit <= 0:
            return []

        results: list[
            VectorSearchResult
        ] = []

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

        return results[
            :limit
        ]

    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Remove um documento do armazenamento.

        Caso o documento não exista, nenhuma exceção será lançada.

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
        Remove todos os documentos armazenados.
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
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        """
        Calcula a similaridade de cosseno entre dois vetores.

        Args:
            vector_a:
                Primeiro vetor.

            vector_b:
                Segundo vetor.

        Returns:
            Valor de similaridade entre os vetores.

        Raises:
            ValueError:
                Caso os vetores possuam dimensões diferentes.
        """

        if len(vector_a) != len(vector_b):
            raise ValueError(
                "Os vetores devem possuir a mesma dimensão."
            )

        dot_product = sum(
            value_a * value_b
            for value_a, value_b in zip(
                vector_a,
                vector_b,
            )
        )

        magnitude_a = math.sqrt(
            sum(
                value * value
                for value in vector_a
            )
        )

        magnitude_b = math.sqrt(
            sum(
                value * value
                for value in vector_b
            )
        )

        if (
            magnitude_a == 0
            or magnitude_b == 0
        ):
            return 0.0

        return (
            dot_product
            / (
                magnitude_a
                * magnitude_b
            )
        )