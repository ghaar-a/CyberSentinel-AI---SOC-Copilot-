from __future__ import annotations

from abc import ABC, abstractmethod

from src.retrieval.retrieved_chunk import RetrievedChunk


class PromptProvider(ABC):
    """
    Contrato responsável pela construção do prompt
    enviado ao modelo de linguagem.

    O Prompt Provider recebe os chunks recuperados
    pela estratégia de busca e os transforma em um
    prompt final para o LLM.

    Dessa forma, o mecanismo de recuperação permanece
    desacoplado da construção do prompt.
    """

    @abstractmethod
    def build_prompt(
        self,
        user_question: str,
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:
        """
        Constrói o prompt final.

        Args:
            user_question:
                Pergunta realizada pelo usuário.

            retrieved_chunks:
                Chunks recuperados pela camada de Retrieval.

        Returns:
            Prompt completo.
        """
        raise NotImplementedError