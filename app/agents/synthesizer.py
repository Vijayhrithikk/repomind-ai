from app.core.gemini import GeminiClient


class Synthesizer:

    def __init__(self):

        self.gemini = GeminiClient()

    def synthesize(
        self,
        question: str,
        results: dict,
    ):

        context = ""

        for tool, result in results.items():

            context += f"""

        TOOL: {tool}

        RESULT:
        {result}

        ----------------
        """

        prompt = f"""
        You are a senior software architect.

        Question:

        {question}

        Tool Results:

        {context}

        Your task:

        1. Review all tool outputs.
        2. Identify agreements and contradictions.
        3. Combine findings into a single answer.
        4. Prioritize repository-specific evidence.
        5. If a security issue exists, mention it.
        6. If architectural concerns exist, mention them.
        7. If information is insufficient, say so.

        Return a practical engineering answer.
        """

        return self.gemini.generate(prompt)