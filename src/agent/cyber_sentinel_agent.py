from src.knowledge.knowledge_loader import KnowledgeLoader
from src.prompts.prompt_manager import PromptManager
from src.llm.gemini_client import GeminiClient


class CyberSentinelAgent:


    def __init__(
        self,
        knowledge_loader: KnowledgeLoader,
        prompt_manager: PromptManager,
        llm_client: GeminiClient,
    ):

        self.knowledge_loader = knowledge_loader
        self.prompt_manager = prompt_manager
        self.llm_client = llm_client



    def ask(
        self,
        question: str
    ):

        documents = (
            self.knowledge_loader
            .search(question)
        )


        context = "\n\n".join(
            document.content
            for document in documents
        )


        prompt = (
            self.prompt_manager
            .build_prompt(
                question,
                context
            )
        )


        return (
            self.llm_client
            .generate(prompt)
        )