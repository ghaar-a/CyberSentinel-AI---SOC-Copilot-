# Concentra toda comunicação com a API do Google Gemini.
from google import genai
from google.genai import types

from src.config.settings import settings

from src.interfaces.llm_provider import LLMProvider
from src.utils.logger import logger


class GeminiClient(LLMProvider):
    """
    Cliente responsável pela comunicação
    com a API do Google Gemini.
    """

    def __init__(self):

        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY não configurada."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        logger.info(
            "Enviando prompt ao Gemini..."
        )

        response = (
            self.client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.temperature,
                    max_output_tokens=settings.max_output_tokens
                )
            )
        )

        logger.info(
            "Resposta recebida do Gemini."
        )

        return response.text