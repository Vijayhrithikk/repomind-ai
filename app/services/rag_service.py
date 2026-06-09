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
        relationships = investigation["relationships"]

        context = ""

        for function in functions:

            context += f"""
        Function:
        {function['function_name']}

        File:
        {function['file_path']}

        Code:
        {function['content']}

        --------------------
        """
        context += "\nRelationships:\n\n"

        for caller, callees in relationships.items():

            context += (
                f"{caller} -> "
                f"{', '.join(callees)}\n"
            )

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