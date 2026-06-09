from app.core.gemini import GeminiClient
from app.tools.function_tools import read_function
from app.graph.repository import GraphRepository


class ExplainService:

    def __init__(self):
        self.gemini = GeminiClient()
        self.graph = GraphRepository()

    def explain(
        self,
        function_name: str,
    ):

        function = read_function(
            function_name
        )

        if not function:
            return {
                "error": "function not found"
            }

        calls = self.graph.get_calls(
            function_name
        )

        prompt = f"""
Explain this Go function.

Function:
{function_name}

Calls:
{calls}

Code:
{function['content']}

Explain:

1. Purpose
2. Inputs
3. Outputs
4. Flow
5. Dependencies
"""

        explanation = self.gemini.generate(
            prompt
        )

        return {
            "function": function_name,
            "calls": calls,
            "explanation": explanation,
        }