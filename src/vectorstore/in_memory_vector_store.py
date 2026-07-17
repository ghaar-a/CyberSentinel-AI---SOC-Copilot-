from typing import Dict, List
import math

from src.interfaces.vector_store import VectorStore
from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class InMemoryVectorStore(VectorStore):
    """
    Implementação simples de armazenamento vetorial em memória.

    Esta classe existe para validar a arquitetura de recuperação
    vetorial antes da introdução de soluções especializadas como:

    - FAISS
    - ChromaDB
    - PostgreSQL com pgvector

    A implementação utiliza similaridade do cosseno para
    comparar vetores.
    """

    def __init__(self) -> None:
        """
        Inicializa o armazenamento interno.

        A estrutura utiliza um dicionário onde a chave é o
        identificador do documento e o valor é o documento vetorial.
        """

        self._documents: Dict[str, VectorDocument] = {}

    def add(
        self,
        document: VectorDocument
    ) -> None:
        """
        Adiciona um documento vetorial ao armazenamento.

        Caso já exista um documento com o mesmo identificador,
        ele será substituído.

        Args:
            document:
                Documento contendo conteúdo, metadados e embedding.
        """

        self._documents[document.id] = document

    def add_many(
        self,
        documents: List[VectorDocument]
    ) -> None:
        """
        Adiciona múltiplos documentos vetoriais.

        Args:
            documents:
                Lista de documentos a serem armazenados.
        """

        for document in documents:
            self.add(document)

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> List[VectorSearchResult]:
        """
        Realiza uma busca por similaridade.

        Cada documento armazenado é comparado com o vetor
        recebido utilizando similaridade do cosseno.

        Args:
            query_vector:
                Vetor representante da consulta.

            top_k:
                Quantidade máxima de resultados retornados.

        Returns:
            Lista ordenada dos documentos mais similares.
        """

        results: List[VectorSearchResult] = []

        for document in self._documents.values():

            similarity = self._cosine_similarity(
                query_vector,
                document.embedding
            )

            results.append(
                VectorSearchResult(
                    document=document,
                    score=similarity
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True
        )

        return results[:top_k]

    def delete(
        self,
        document_id: str
    ) -> None:
        """
        Remove um documento pelo identificador.

        Args:
            document_id:
                Identificador do documento.
        """

        self._documents.pop(
            document_id,
            None
        )

    def clear(self) -> None:
        """
        Remove todos os documentos armazenados.
        """

        self._documents.clear()

    @staticmethod
    def _cosine_similarity(
        vector_a: List[float],
        vector_b: List[float]
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
            Valor de similaridade entre os vetores.
        """

        if len(vector_a) != len(vector_b):
            raise ValueError(
                "Os vetores precisam possuir a mesma dimensão."
            )

        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(
                a * a
                for a in vector_a
            )
        )

        magnitude_b = math.sqrt(
            sum(
                b * b
                for b in vector_b
            )
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (
            magnitude_a * magnitude_b
        )