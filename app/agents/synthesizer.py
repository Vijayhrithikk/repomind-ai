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
        available_tools = list(results.keys())

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

Available Evidence:

{available_tools}

You may only make conclusions supported
by the available tool results.

If information is missing,
explicitly say what additional tool
or investigation would be required.

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