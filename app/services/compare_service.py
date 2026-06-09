from app.core.gemini import GeminiClient
from app.tools.function_tools import read_function


class CompareService:

    def __init__(self):
        self.gemini = GeminiClient()

    def compare(
        self,
        func1: str,
        func2: str,
    ):

        first = read_function(func1)
        second = read_function(func2)

        if not first or not second:
            return {
                "error": "function not found"
            }

        prompt = f"""
        
Compare these two Go functions.

Function A:
{first['content']}

Function B:
{second['content']}

Explain:

1. Purpose
2. Similarities
3. Differences
4. Dependencies
5. When each should be used
"""

        result = self.gemini.generate(
            prompt
        )

        return {
            "comparison": result
        }