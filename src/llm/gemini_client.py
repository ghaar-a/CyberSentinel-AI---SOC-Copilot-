from google import genai
from google.genai import types

from src.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
)


class GeminiClient:


    def __init__(self):

        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY não configurada."
            )


        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )



    def generate(
        self,
        prompt: str
    ) -> str:


        response = (
            self.client.models.generate_content(
                model=GEMINI_MODEL,

                contents=prompt,

                config=types.GenerateContentConfig(
                    temperature=TEMPERATURE,
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                ),
            )
        )


        return response.text