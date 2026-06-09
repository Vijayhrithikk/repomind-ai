from app.core.gemini import GeminiClient
from app.tools.function_tools import read_function


class RepositorySummaryService:

    def __init__(self):
        self.gemini = GeminiClient()

    def summarize(
        self,
        functions,
    ):

        context = ""

        for function in functions[:20]:

            context += f"""
Function:
{function['function_name']}

Code:
{function['content'][:1000]}

--------------------
"""

        prompt = f"""
Analyze these repository functions.

Explain:

1. What problem this repository solves
2. Main features
3. Architecture
4. Technologies used

Code:

{context}
"""

        return self.gemini.generate(
            prompt
        )