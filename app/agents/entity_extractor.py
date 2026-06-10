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

        Determine whether the user is asking about:

        1. A Go function
        2. A repository topic

        Return ONLY JSON.

        Examples:

        Question:
        Explain Login

        Output:
        {{"kind":"function","value":"Login"}}

        Question:
        Trace SignUp

        Output:
        {{"kind":"function","value":"SignUp"}}

        Question:
        How secure is authentication?

        Output:
        {{"kind":"topic","value":"authentication"}}

        Question:
        How does authorization work?

        Output:
        {{"kind":"topic","value":"authorization"}}

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
               "value" not in entity):
                raise ValueError("missing field")
            return entity 
        except Exception as e:
            print("Entity parse error:", e)
            return {
                "kind":"topic",
                "value": question,
            }