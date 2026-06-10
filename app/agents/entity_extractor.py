from app.core.gemini import GeminiClient


class EntityExtractor:

    def __init__(self):
        self.gemini = GeminiClient()

    def extract(
        self,
        question: str,
    ):

        prompt = f"""
        You are an extraction engine.

        Determine:

        1. Entity kind
        2. Entity value
        3. User intent

        Return ONLY JSON.

        Examples:

        Question:
Explain Login

Output:
{{"kind":"function","value":"Login","intent":"explain"}}

Question:
Trace Login

Output:
{{"kind":"function","value":"Login","intent":"trace"}}

Question:
How secure is authentication?

Output:
{{"kind":"topic","value":"authentication","intent":"security"}}

Question:
How does authentication work?

Output:
{{"kind":"topic","value":"authentication","intent":"architecture"}}

Question:
Compare Login and SignUp

Output:
{{"kind":"function","value":"Login","intent":"compare"}}

        Question:
        {question}
        """

        response = self.gemini.generate(prompt)
        print("Raw:", response)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        import json

        try:
            entity= json.loads(response)
            if("kind" not in entity or
               "value" not in entity
               or "intent" not in entity):
                raise ValueError("missing field")
            return entity 
        except Exception as e:
            print("Entity parse error:", e)
            return {
                "kind":"topic",
                "value": question,
                "intent": "unknown",
            }