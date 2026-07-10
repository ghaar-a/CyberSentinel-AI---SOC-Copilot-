from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Contrato para qualquer modelo de linguagem.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Gera uma resposta utilizando um LLM.
        """
        raise NotImplementedError