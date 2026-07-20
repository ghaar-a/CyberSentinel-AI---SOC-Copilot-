from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Configurações globais da aplicação.

    As configurações podem ser definidas através de variáveis
    de ambiente ou do arquivo .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str = Field(
        validation_alias="GEMINI_API_KEY",
    )

    gemini_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias="GEMINI_MODEL",
    )

    temperature: float = 0.2

    max_output_tokens: int = 2048

    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL",
    )

    chroma_collection_name: str = Field(
        default="cybersentinel_knowledge",
        validation_alias="CHROMA_COLLECTION_NAME",
    )

    chroma_persist_directory: str = Field(
        default=".chroma",
        validation_alias="CHROMA_PERSIST_DIRECTORY",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Retorna uma única instância das configurações.
    """

    return Settings()


settings = get_settings()

DATA_DIR = PROJECT_ROOT / "data"

KNOWLEDGE_DIR = DATA_DIR / "knowledge"

PROMPTS_DIR = PROJECT_ROOT / "src" / "prompts"

DOCS_DIR = PROJECT_ROOT / "docs"

CHROMA_DIR = PROJECT_ROOT / settings.chroma_persist_directory