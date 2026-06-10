from app.core.gemini import GeminiClient
from app.agents.evidence import Evidence
from app.agents.result_summarizer import (
    summarize_result,
)


class Synthesizer:

    def __init__(self):

        self.gemini = GeminiClient()

    def synthesize(
        self,
        question: str,
        results: dict,
        notes: list[str] | None = None,
        evidence: Evidence | None = None,
    ):

        context = ""

        for tool, result in results.items():

            context += summarize_result(
                tool,
                result,
            )

            context += "\n----------------\n"

        notes_text = ""

        if notes:

            notes_text = "\n".join(
                f"- {note}"
                for note in notes
            )

        observations = []
        unknowns = []

        if evidence:

            observations = (evidence.observations)

            unknowns = (evidence.unknowns)

        prompt = f"""
You are a senior software architect.

Question:

{question}

Observed Facts:

{observations}

Unknowns:

{unknowns}

Investigation Notes:

{notes_text}

Tool Summaries:

{context}

Rules:

1. Clearly separate:
   - Observed
   - Inferred
   - Unknown

2. Never claim something was observed
   unless it appears in Observed Facts.

3. If evidence is insufficient,
   explicitly say so.

4. Use tool summaries only to support
   observations and inferences.

Return a practical engineering answer.
"""

        return self.gemini.generate(prompt)