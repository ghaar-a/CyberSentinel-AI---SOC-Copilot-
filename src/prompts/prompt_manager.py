from pathlib import Path

from src.retrieval.retrieved_chunk import RetrievedChunk
from src.interfaces.prompt_provider import PromptProvider

from src.prompts.context_formatter import ContextFormatter
from src.prompts.prompt_builder import PromptBuilder
from src.prompts.prompt_loader import PromptLoader


class PromptManager(PromptProvider):
    """
    Fachada da Prompt Engine.

    Responsável por coordenar
    toda a construção do prompt.
    """

    def __init__(
        self,
        prompts_directory: Path,
    ) -> None:

        self.loader = PromptLoader(
            prompts_directory
        )

        self.formatter = ContextFormatter()

        self.builder = PromptBuilder()

    def build_prompt(
        self,
        user_question: str,
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:

        system_prompt = self.loader.load(
            "system_prompt.md"
        )

        guardrails = self.loader.load(
            "guardrails.md"
        )

        response_template = self.loader.load(
            "response_template.md"
        )

        knowledge_context = (
            self.formatter.format(
                retrieved_chunks
            )
        )

        return self.builder.build(
            system_prompt=system_prompt,
            guardrails=guardrails,
            knowledge_context=knowledge_context,
            response_template=response_template,
            user_question=user_question,
        )

    def clear_cache(
        self,
    ) -> None:

        self.loader.clear_cache()