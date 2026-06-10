class Planner:

    def plan(
        self,
        question: str,
        entity: dict,
    ):

        intent = entity.get(
            "intent",
            "rag",
        )

        if intent == "trace":

            return {
                "tools": ["trace"]
            }

        if intent == "explain":

            return {
                "tools": ["explain"]
            }

        if intent == "security":

            return {
                "tools": [
                    "trace",
                    "security_review",
                ]
            }

        if intent == "architecture":

            return {
                "tools": [
                    "architecture"
                ]
            }

        return {
            "tools": ["rag"]
        }