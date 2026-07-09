from pathlib import Path


class PromptManager:


    def __init__(
        self,
        prompts_path: Path
    ):

        self.prompts_path = prompts_path



    def load_prompt(
        self,
        filename: str
    ):

        file = (
            self.prompts_path /
            filename
        )

        return file.read_text(
            encoding="utf-8"
        )



    def build_prompt(
        self,
        question: str,
        knowledge: str
    ):


        system = self.load_prompt(
            "system_prompt.md"
        )


        guardrails = self.load_prompt(
            "guardrails.md"
        )


        return f"""
{system}


{guardrails}


Knowledge Context:

{knowledge}


User Question:

{question}
"""