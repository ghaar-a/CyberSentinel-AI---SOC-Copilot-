# Orquestra a Prompt Engine e fornece uma interface única para o restante da aplicação.
from pathlib import Path
from typing import List

from src.knowledge.knowledge_document import KnowledgeDocument

from src.prompts.context_formatter import ContextFormatter
from src.prompts.prompt_builder import PromptBuilder
from src.prompts.prompt_loader import PromptLoader


class PromptManager:
    """
    Fachada da Prompt Engine.

    Responsável por fornecer
    um único ponto de acesso
    para construção de prompts.
    """

    def __init__(
        self,
        prompts_directory: Path
    ):

        self.loader = PromptLoader(
            prompts_directory
        )

        self.formatter = ContextFormatter()

        self.builder = PromptBuilder()

    def build_prompt(
        self,
        user_question: str,
        documents: List[KnowledgeDocument]
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
                documents
            )
        )

        return self.builder.build(
            system_prompt=system_prompt,
            guardrails=guardrails,
            knowledge_context=knowledge_context,
            response_template=response_template,
            user_question=user_question
        )

    def clear_cache(self):

        self.loader.clear_cache()