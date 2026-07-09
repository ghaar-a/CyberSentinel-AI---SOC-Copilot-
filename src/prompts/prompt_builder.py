# Monta o prompt final a partir dos componentes.
class PromptBuilder:
    """
    Responsável por construir
    o prompt enviado ao LLM.
    """

    def build(
        self,
        system_prompt: str,
        guardrails: str,
        knowledge_context: str,
        response_template: str,
        user_question: str
    ) -> str:

        return f"""
========================
SYSTEM PROMPT
========================

{system_prompt}

========================
GUARDRAILS
========================

{guardrails}

========================
KNOWLEDGE BASE
========================

{knowledge_context}

========================
USER QUESTION
========================

{user_question}

========================
RESPONSE TEMPLATE
========================

{response_template}
""".strip()