from app.core.gemini import GeminiClient
from app.services.repository_explorer import (
    RepositoryExplorer,
)


class RAGService:

    def __init__(self):
        self.explorer = RepositoryExplorer()
        self.gemini = GeminiClient()

    def ask(
        self,
        question: str,
    ):

        investigation = self.explorer.investigate(
            question
        )

        functions = investigation["functions"]
        sources = investigation["sources"]

        context = ""

        for function in functions:

            context += f"""
Function:
{function['function_name']}

Code:
{function['content']}

--------------------
"""

        prompt = f"""
You are an expert Go software engineer.

Answer ONLY using the provided code.

If the answer cannot be determined,
say so.

Context:

{context}

Question:

{question}
"""

        answer = self.gemini.generate(
            prompt
        )

        return {
            "answer": answer,
            "sources": sources,
        }