from __future__ import annotations

from pathlib import Path
from typing import Any, TypedDict, cast

import chromadb
from chromadb.api.types import (
    Metadata,
    QueryResult,
)

from src.chunking.chunk import Chunk
from src.interfaces.vector_store import VectorStore
from src.utils.logger import logger
from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class ChunkMetadata(TypedDict):
    """
    Representa os metadados utilizados internamente pela aplicação
    para reconstruir um Chunk.

    Esta estrutura representa o contrato de dados da camada de domínio
    e não deve ser confundida com o tipo Metadata utilizado diretamente
    pela API do ChromaDB.
    """

    document_name: str
    category: str
    source_path: str
    chunk_index: int


class ChromaVectorStore(VectorStore):
    """
    Implementação persistente de VectorStore utilizando ChromaDB.

    O ChromaDB é utilizado como infraestrutura concreta de armazenamento
    e recuperação vetorial.

    Esta classe implementa o contrato VectorStore e, portanto, as camadas
    superiores da aplicação não possuem conhecimento sobre ChromaDB.

    O armazenamento mantém:

    - embedding do documento;
    - identificador único;
    - conteúdo original;
    - metadados necessários para reconstrução do contexto.

    A persistência é realizada pelo próprio ChromaDB através do diretório
    configurado no cliente persistente.

    A implementação utiliza distância cosseno para a busca vetorial.
    A distância retornada pelo ChromaDB é convertida para uma pontuação
    de similaridade através da fórmula:

    similarity = 1 - distance
    """

    def __init__(
        self,
        persist_directory: str,
        collection_name: str = "cybersentinel_knowledge",
    ) -> None:
        """
        Inicializa o armazenamento vetorial ChromaDB.

        Args:
            persist_directory:
                Diretório utilizado pelo ChromaDB para persistir os dados.

            collection_name:
                Nome da coleção responsável por armazenar os embeddings.
        """

        logger.info(
            "Inicializando ChromaDB em: %s",
            persist_directory,
        )

        self._client = chromadb.PersistentClient(
            path=persist_directory,
        )

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            configuration={
                "hnsw": {
                    "space": "cosine",
                },
            },
        )

        logger.info(
            "Coleção ChromaDB inicializada: %s",
            collection_name,
        )

    def add(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Adiciona ou atualiza um documento vetorial.

        O identificador do VectorDocument é utilizado como identificador
        único dentro da coleção ChromaDB.

        Args:
            document:
                Documento vetorial que será persistido.
        """

        self._collection.upsert(
            ids=[
                document.id,
            ],
            embeddings=[
                document.vector,
            ],
            documents=[
                document.chunk.content,
            ],
            metadatas=[
                self._build_chroma_metadata(
                    document,
                ),
            ],
        )

    def add_many(
        self,
        documents: list[VectorDocument],
    ) -> None:
        """
        Adiciona ou atualiza múltiplos documentos vetoriais.

        Args:
            documents:
                Lista de documentos vetoriais que serão persistidos.
        """

        if not documents:
            return

        self._collection.upsert(
            ids=[
                document.id
                for document in documents
            ],
            embeddings=[
                document.vector
                for document in documents
            ],
            documents=[
                document.chunk.content
                for document in documents
            ],
            metadatas=[
                self._build_chroma_metadata(
                    document,
                )
                for document in documents
            ],
        )

        logger.info(
            "Documentos vetoriais persistidos no ChromaDB: %d",
            len(documents),
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[VectorSearchResult]:
        """
        Executa uma busca por similaridade vetorial.

        O ChromaDB retorna os documentos ordenados por distância.
        Como a coleção utiliza distância cosseno, a distância é convertida
        para uma pontuação de similaridade.

        Args:
            query_vector:
                Vetor correspondente à consulta.

            limit:
                Quantidade máxima de resultados.

        Returns:
            Lista de resultados ordenados pela maior similaridade.

        Raises:
            ValueError:
                Caso o vetor da consulta esteja vazio.

            ValueError:
                Caso o limite seja menor ou igual a zero.
        """

        if not query_vector:
            raise ValueError(
                "O vetor da consulta não pode estar vazio.",
            )

        if limit <= 0:
            raise ValueError(
                "O limite da busca deve ser maior que zero.",
            )

        collection_size = self.size()

        if collection_size == 0:
            return []

        results = self._collection.query(
            query_embeddings=[
                query_vector,
            ],
            n_results=min(
                limit,
                collection_size,
            ),
            include=[
                "embeddings",
                "documents",
                "metadatas",
                "distances",
            ],
        )

        return self._build_search_results(
            results,
        )

    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Remove um documento vetorial do ChromaDB.

        Args:
            document_id:
                Identificador do documento.
        """

        self._collection.delete(
            ids=[
                document_id,
            ],
        )

    def clear(
        self,
    ) -> None:
        """
        Remove todos os documentos armazenados na coleção atual.

        A coleção é removida e recriada para garantir que o índice
        seja completamente limpo.
        """

        collection_name = self._collection.name

        self._client.delete_collection(
            name=collection_name,
        )

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            configuration={
                "hnsw": {
                    "space": "cosine",
                },
            },
        )

        logger.info(
            "Coleção ChromaDB limpa: %s",
            collection_name,
        )

    def size(
        self,
    ) -> int:
        """
        Retorna a quantidade de documentos indexados.

        Returns:
            Quantidade de documentos armazenados na coleção.
        """

        return self._collection.count()

    @staticmethod
    def _build_chroma_metadata(
        document: VectorDocument,
    ) -> Metadata:
        """
        Constrói os metadados no formato esperado pelo ChromaDB.

        Este método atua como uma fronteira entre o modelo interno
        de dados da aplicação e o tipo de metadados exigido pela
        infraestrutura ChromaDB.

        Args:
            document:
                Documento vetorial que será convertido em metadados.

        Returns:
            Metadados compatíveis com a API do ChromaDB.
        """

        metadata: Metadata = {
            "document_name": document.chunk.document_name,
            "category": document.chunk.category,
            "source_path": str(
                document.chunk.source_path,
            ),
            "chunk_index": document.chunk.index,
        }

        return metadata

    @classmethod
    def _build_search_results(
        cls,
        results: QueryResult,
    ) -> list[VectorSearchResult]:
        """
        Converte a resposta do ChromaDB em resultados da aplicação.

        A resposta do ChromaDB possui resultados agrupados por consulta.
        Como o VectorStore executa uma única consulta por vez, apenas
        o primeiro grupo de cada campo é processado.

        Args:
            results:
                Resultado retornado pelo ChromaDB.

        Returns:
            Lista de resultados vetoriais convertidos para o domínio
            da aplicação.
        """

        ids = cls._extract_result_group(
            results.get("ids"),
        )

        embeddings = cls._extract_result_group(
            results.get("embeddings"),
        )

        documents = cls._extract_result_group(
            results.get("documents"),
        )

        metadatas = cls._extract_result_group(
            results.get("metadatas"),
        )

        distances = cls._extract_result_group(
            results.get("distances"),
        )

        if not (
            ids
            and embeddings
            and documents
            and metadatas
            and distances
        ):
            return []

        search_results: list[
            VectorSearchResult
        ] = []

        for (
            document_id,
            vector,
            content,
            metadata,
            distance,
        ) in zip(
            ids,
            embeddings,
            documents,
            metadatas,
            distances,
            strict=True,
        ):
            if not isinstance(
                document_id,
                str,
            ):
                continue

            if not isinstance(
                content,
                str,
            ):
                continue

            if not isinstance(
                distance,
                (int, float),
            ):
                continue

            chunk_metadata = cls._validate_metadata(
                metadata,
            )

            if chunk_metadata is None:
                logger.warning(
                    "Metadados inválidos encontrados para o documento: %s",
                    document_id,
                )
                continue

            chunk = cls._build_chunk(
                document_id=document_id,
                content=content,
                metadata=chunk_metadata,
            )

            vector_document = VectorDocument(
                id=document_id,
                chunk=chunk,
                vector=[
                    float(value)
                    for value in vector
                ],
            )

            similarity = cls._distance_to_similarity(
                distance,
            )

            search_results.append(
                VectorSearchResult(
                    document=vector_document,
                    score=similarity,
                ),
            )

        return search_results

    @staticmethod
    def _extract_result_group(
        value: Any,
    ) -> list[Any]:
        """
        Extrai o primeiro grupo de resultados retornado pelo ChromaDB.

        A API de consulta do ChromaDB retorna resultados agrupados por
        consulta. Como o VectorStore executa uma única consulta por vez,
        apenas o primeiro grupo é utilizado.

        Args:
            value:
                Valor retornado pelo ChromaDB.

        Returns:
            Lista contendo os resultados da primeira consulta.
            Retorna uma lista vazia caso o valor seja inexistente
            ou possua formato inesperado.
        """

        if value is None:
            return []

        if not isinstance(
            value,
            list,
        ):
            return []

        if not value:
            return []

        first_group = value[0]

        if first_group is None:
            return []

        if not isinstance(
            first_group,
            list,
        ):
            return []

        return first_group

    @staticmethod
    def _validate_metadata(
        metadata: Any,
    ) -> ChunkMetadata | None:
        """
        Valida e normaliza os metadados retornados pelo ChromaDB.

        Este método representa a fronteira de entrada dos dados externos
        na aplicação. Somente após a validação os metadados são convertidos
        para o formato interno ChunkMetadata.

        Args:
            metadata:
                Metadados retornados pela consulta ao ChromaDB.

        Returns:
            Metadados tipados caso sejam válidos.
            None caso os metadados estejam incompletos ou inválidos.
        """

        if not isinstance(
            metadata,
            dict,
        ):
            return None

        document_name = metadata.get(
            "document_name",
        )

        category = metadata.get(
            "category",
        )

        source_path = metadata.get(
            "source_path",
        )

        chunk_index = metadata.get(
            "chunk_index",
        )

        if not isinstance(
            document_name,
            str,
        ):
            return None

        if not isinstance(
            category,
            str,
        ):
            return None

        if not isinstance(
            source_path,
            str,
        ):
            return None

        if not isinstance(
            chunk_index,
            int,
        ):
            return None

        return {
            "document_name": document_name,
            "category": category,
            "source_path": source_path,
            "chunk_index": chunk_index,
        }

    @staticmethod
    def _build_chunk(
        document_id: str,
        content: str,
        metadata: ChunkMetadata,
    ) -> Chunk:
        """
        Reconstrói um Chunk a partir dos dados persistidos no ChromaDB.

        Args:
            document_id:
                Identificador único do chunk.

            content:
                Conteúdo textual armazenado.

            metadata:
                Metadados validados e normalizados.

        Returns:
            Instância reconstruída de Chunk.
        """

        return Chunk(
            id=document_id,
            document_name=metadata[
                "document_name"
            ],
            category=metadata[
                "category"
            ],
            source_path=Path(
                metadata[
                    "source_path"
                ],
            ),
            index=metadata[
                "chunk_index"
            ],
            content=content,
        )

    @staticmethod
    def _distance_to_similarity(
        distance: float,
    ) -> float:
        """
        Converte distância cosseno em pontuação de similaridade.

        Args:
            distance:
                Distância cosseno retornada pelo ChromaDB.

        Returns:
            Pontuação de similaridade.
        """

        return 1.0 - float(
            distance,
        )