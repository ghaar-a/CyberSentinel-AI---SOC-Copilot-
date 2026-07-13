from __future__ import annotations

from src.interfaces.chunk_provider import ChunkProvider
from src.retrieval.retrieval_strategy import RetrievalStrategy
from src.retrieval.retrieved_chunk import RetrievedChunk


class KeywordChunkRetriever(RetrievalStrategy):
    """
    Recuperação baseada em palavras-chave.
    """

    def __init__(
        self,
        provider: ChunkProvider,
    ) -> None:

        self.provider = provider

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:

        terms = {
            term.lower()
            for term in query.split()
        }

        ranking: list[
            tuple[int, RetrievedChunk]
        ] = []

        for chunk in self.provider.get_chunks():

            searchable_text = chunk.content.lower()

            score = sum(
                term in searchable_text
                for term in terms
            )

            if score > 0:

                ranking.append(
                    (
                        score,
                        RetrievedChunk(
                            chunk=chunk,
                            score=float(score),
                            rank=0,
                        ),
                    )
                )

        ranking.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        results = []

        for position, (_, item) in enumerate(ranking):

            item.rank = position + 1

            results.append(item)

        return results[:limit]