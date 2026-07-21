from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb

from src.chunking.chunk import Chunk
from src.interfaces.vector_store import VectorStore
from src.utils.logger import logger
from src.vectorstore.vector_document import VectorDocument
from src.vectorstore.vector_search_result import VectorSearchResult


class ChromaVectorStore(VectorStore):
    """
    Implementação persistente de VectorStore utilizando ChromaDB.

    O ChromaDB é utilizado como infraestrutura concreta de armazenamento
    e recuperação vetorial.

    Esta classe implementa o contrato VectorStore e, portanto, as camadas
    superiores da aplicação não possuem conhecimento sobre a implementação
    concreta utilizada para persistência e busca vetorial.

    Cada documento armazenado contém:

    - identificador único;
    - embedding;
    - conteúdo textual original;
    - metadados necessários para reconstrução do Chunk.

    A coleção utiliza distância cosseno para calcular a proximidade
    entre os embeddings.

    A distância retornada pelo ChromaDB é convertida para uma pontuação
    de similaridade através da fórmula:

        similarity = 1 - distance

    Quanto maior o valor da similaridade, maior a proximidade semântica
    entre os vetores.
    """

    _DISTANCE_SPACE = "cosine"

    def __init__(
        self,
        persist_directory: str,
        collection_name: str = "cybersentinel_knowledge",
    ) -> None:
        """
        Inicializa o armazenamento vetorial persistente.

        Args:
            persist_directory:
                Diretório utilizado pelo ChromaDB para persistência dos dados.

            collection_name:
                Nome da collection utilizada para armazenar os embeddings.
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
                    "space": self._DISTANCE_SPACE,
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
        único dentro da collection do ChromaDB.

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
                self._build_metadata(
                    document,
                ),
            ],
        )

        logger.debug(
            "Documento vetorial persistido: %s",
            document.id,
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
            logger.warning(
                "Nenhum documento vetorial recebido para persistência.",
            )
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
                self._build_metadata(
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

        O ChromaDB retorna os resultados ordenados por distância.
        Como a collection utiliza distância cosseno, a distância é
        convertida para uma pontuação de similaridade.

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

        ids = results.get(
            "ids",
            [[]],
        )[0]

        embeddings = results.get(
            "embeddings",
            [[]],
        )[0]

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

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
            if content is None:
                logger.warning(
                    "Documento sem conteúdo retornado pelo ChromaDB: %s",
                    document_id,
                )
                continue

            if metadata is None:
                logger.warning(
                    "Documento sem metadados retornado pelo ChromaDB: %s",
                    document_id,
                )
                continue

            chunk = self._build_chunk(
                document_id=document_id,
                content=content,
                metadata=metadata,
            )

            vector_document = VectorDocument(
                id=document_id,
                chunk=chunk,
                vector=list(vector),
            )

            similarity = self._distance_to_similarity(
                distance,
            )

            search_results.append(
                VectorSearchResult(
                    document=vector_document,
                    score=similarity,
                )
            )

        return search_results

    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Remove um documento vetorial do ChromaDB.

        Caso o identificador não exista, nenhuma exceção é lançada.

        Args:
            document_id:
                Identificador do documento que será removido.
        """

        self._collection.delete(
            ids=[
                document_id,
            ],
        )

        logger.debug(
            "Documento vetorial removido: %s",
            document_id,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove todos os documentos da collection atual.

        A collection é removida e recriada para garantir que o índice
        vetorial seja completamente reconstruído.

        A configuração de distância utilizada pela collection original
        é preservada na nova collection.
        """

        collection_name = self._collection.name

        logger.info(
            "Limpando coleção ChromaDB: %s",
            collection_name,
        )

        self._client.delete_collection(
            name=collection_name,
        )

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            configuration={
                "hnsw": {
                    "space": self._DISTANCE_SPACE,
                },
            },
        )

        logger.info(
            "Coleção ChromaDB recriada: %s",
            collection_name,
        )

    def size(
        self,
    ) -> int:
        """
        Retorna a quantidade de documentos indexados.

        Returns:
            Quantidade de documentos armazenados na collection.
        """

        return self._collection.count()

    @staticmethod
    def _build_metadata(
        document: VectorDocument,
    ) -> dict[str, Any]:
        """
        Constrói os metadados persistidos junto ao embedding.

        Args:
            document:
                Documento vetorial que será convertido em metadados.

        Returns:
            Dicionário contendo os metadados necessários para reconstrução
            do Chunk.
        """

        return {
            "document_name": document.chunk.document_name,
            "category": document.chunk.category,
            "source_path": str(
                document.chunk.source_path,
            ),
            "chunk_index": document.chunk.index,
        }

    @staticmethod
    def _build_chunk(
        document_id: str,
        content: str,
        metadata: dict[str, Any],
    ) -> Chunk:
        """
        Reconstrói um Chunk a partir dos dados persistidos no ChromaDB.

        Args:
            document_id:
                Identificador único do chunk.

            content:
                Conteúdo textual armazenado.

            metadata:
                Metadados persistidos junto ao documento.

        Returns:
            Instância reconstruída de Chunk.
        """

        return Chunk(
            id=document_id,
            document_name=str(
                metadata["document_name"],
            ),
            category=str(
                metadata["category"],
            ),
            source_path=Path(
                str(
                    metadata["source_path"],
                ),
            ),
            index=int(
                metadata["chunk_index"],
            ),
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