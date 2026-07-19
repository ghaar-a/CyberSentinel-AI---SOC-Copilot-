from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.interfaces.embedding_provider import EmbeddingProvider


class SentenceTransformersEmbeddingProvider(
    EmbeddingProvider,
):
    """
    Implementação de EmbeddingProvider utilizando
    modelos da biblioteca Sentence Transformers.

    O modelo é executado localmente, permitindo gerar
    embeddings sem depender de uma API externa.

    A mesma implementação é utilizada tanto para indexar
    os chunks da base de conhecimento quanto para transformar
    consultas do usuário em vetores.
    """

    def __init__(
        self,
        model_name: str,
    ) -> None:
        """
        Inicializa o provedor de embeddings.

        Args:
            model_name:
                Nome do modelo Sentence Transformers utilizado
                para gerar os embeddings.
        """

        self._model = SentenceTransformer(
            model_name,
        )

    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        """
        Gera embeddings para os chunks informados.

        Args:
            chunks:
                Chunks que serão transformados em vetores.

        Returns:
            Lista de embeddings associados aos seus chunks.
        """

        if not chunks:
            return []

        texts = [
            chunk.content
            for chunk in chunks
        ]

        vectors = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return [
            Embedding(
                chunk=chunk,
                vector=vector.tolist(),
            )
            for chunk, vector in zip(
                chunks,
                vectors,
            )
        ]

    def generate_query_embedding(
        self,
        query: str,
    ) -> list[float]:
        """
        Gera um embedding para uma consulta textual.

        A consulta utiliza o mesmo modelo e as mesmas regras
        de normalização aplicadas aos embeddings dos documentos.

        Args:
            query:
                Consulta textual realizada pelo usuário.

        Returns:
            Vetor normalizado correspondente à consulta.
        """

        if not query.strip():
            return []

        vector = self._model.encode(
            query.strip(),
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return vector.tolist()