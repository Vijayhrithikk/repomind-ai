from app.core.gemini import GeminiClient


class Synthesizer:

    def __init__(self):

        self.gemini = GeminiClient()

    def synthesize(
        self,
        question: str,
        results: dict,
    ):

        prompt = f"""
You are a senior software architect.

Question:

{question}

Tool Results:

{results}

Generate a final answer.

Use the tool results.

Be concise and practical.
"""

        return self.gemini.generate(
            prompt
        )