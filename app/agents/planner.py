from app.core.gemini import GeminiClient
import json


class Planner:

    def __init__(self):
        self.gemini = GeminiClient()

    def plan(self,question: str,):
        prompt = f"""
        You are a repository agent planner.

        Available tools:

        trace
        explain
        security_review
        rag

        Return ONLY valid JSON.

        Examples:

        Question:
        How secure is authentication?

        Output:
        {{"tools":["trace","explain","security_review"]}}

        Question:
        Trace login flow

        Output:
        {{"tools":["trace"]}}

        Question:
        Explain Login

        Output:
        {{"tools":["explain"]}}

        Question:
        {question}
        """

        response = self.gemini.generate(prompt)

        response=self.clean_json(response)
        print("Plan:",response)

        try:
            return json.loads(response)
        except Exception as e:

            print("Planner error:",e)
            return{
                "tools":["rag"]
            }

    def clean_json(
        self,
        text: str,
    ):

        text = text.strip()

        if text.startswith("```json"):
            text = text.replace(
                "```json",
                "",
                1,
            )

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()