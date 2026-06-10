from app.core.gemini import GeminiClient


class Synthesizer:

    def __init__(self):

        self.gemini = GeminiClient()

    def synthesize(
        self,
        question: str,
        results: dict,
        notes: list[str] = None,
    ):

        context = ""

        for tool, result in results.items():

            context += f"""

TOOL:
{tool}

RESULT:
{result}

------------------------
"""

        notes_text = ""

        if notes:

            notes_text = "\n".join(f"- {note}" for note in notes)

        prompt = f"""
You are a senior software architect.

Question:

{question}

Investigation Notes:

{notes_text}

Tool Results:

{context}

Your task:

1. Review all findings.
2. Identify important observations.
3. Combine evidence from multiple tools.
4. Mention security concerns if present.
5. Mention architectural concerns if present.
6. Use repository-specific evidence.
7. If information is insufficient, say so.

Return a practical engineering answer.
"""

        return self.gemini.generate(prompt)