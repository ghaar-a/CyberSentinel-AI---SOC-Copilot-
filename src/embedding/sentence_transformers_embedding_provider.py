from __future__ import annotations

from sentence_transformers import SentenceTransformer

from src.chunking.chunk import Chunk
from src.embedding.embedding import Embedding
from src.interfaces.embedding_provider import EmbeddingProvider
from src.utils.logger import logger


class SentenceTransformersEmbeddingProvider(EmbeddingProvider):
    """
    Implementação de EmbeddingProvider utilizando Sentence Transformers.

    Esta classe transforma o conteúdo textual dos chunks em vetores
    semânticos utilizando um modelo local de embeddings.

    A implementação permanece desacoplada do restante da aplicação
    através do contrato EmbeddingProvider.

    Dessa forma, a aplicação pode futuramente substituir Sentence
    Transformers por outro provedor sem modificar o EmbeddingGenerator,
    o Retriever ou o agente principal.

    O modelo padrão utilizado é o all-MiniLM-L6-v2, que gera vetores
    de 384 dimensões e apresenta bom equilíbrio entre qualidade,
    velocidade e consumo de recursos para execução em CPU.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        """
        Inicializa o provedor de embeddings.

        O modelo é carregado uma única vez durante a criação do provider
        e permanece em memória para reutilização nas próximas chamadas.

        Args:
            model_name:
                Nome do modelo Sentence Transformers utilizado para
                gerar os embeddings.
        """

        logger.info(
            "Carregando modelo de embeddings: %s",
            model_name,
        )

        self._model = SentenceTransformer(
            model_name,
        )

        self._model_name = model_name

        logger.info(
            "Modelo de embeddings carregado com sucesso: %s",
            model_name,
        )

    @property
    def model_name(self) -> str:
        """
        Retorna o nome do modelo utilizado pelo provider.
        """

        return self._model_name

    def generate(
        self,
        chunks: list[Chunk],
    ) -> list[Embedding]:
        """
        Gera embeddings para uma coleção de chunks.

        Cada chunk é convertido em um vetor numérico que representa
        semanticamente o seu conteúdo.

        Args:
            chunks:
                Lista de chunks que serão transformados em embeddings.

        Returns:
            Lista de objetos Embedding associados aos respectivos chunks.

        Raises:
            ValueError:
                Caso a lista de chunks esteja vazia.
        """

        if not chunks:
            raise ValueError(
                "Não é possível gerar embeddings para uma lista vazia de chunks."
            )

        logger.info(
            "Gerando embeddings para %d chunks...",
            len(chunks),
        )

        texts = [
            chunk.content
            for chunk in chunks
        ]

        vectors = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        embeddings = [
            Embedding(
                chunk=chunk,
                vector=vector.tolist(),
            )
            for chunk, vector in zip(
                chunks,
                vectors,
                strict=True,
            )
        ]

        logger.info(
            "Embeddings gerados com sucesso: %d",
            len(embeddings),
        )

        return embeddings