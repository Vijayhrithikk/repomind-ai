from app.core.gemini import GeminiClient


class EntityExtractor:

    def __init__(self):
        self.gemini = GeminiClient()

    def extract(
        self,
        question: str,
    ):

        prompt = f"""
Extract the primary Go function name.

Return ONLY JSON.

Example:

Question:
Explain Login

Output:
{{"function":"Login"}}

Question:
{question}
"""

        response = self.gemini.generate(prompt)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        import json

        try:
            return json.loads(response)
        except:
            return {
                "function": "Login"
            }