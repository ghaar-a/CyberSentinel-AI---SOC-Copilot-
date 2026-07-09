from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

KNOWLEDGE_DIR = DATA_DIR / "knowledge"

PROMPTS_DIR = PROJECT_ROOT / "src" / "prompts"

DOCS_DIR = PROJECT_ROOT / "docs"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

MODEL_NAME = "gemini-2.5-flash"

TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 2048