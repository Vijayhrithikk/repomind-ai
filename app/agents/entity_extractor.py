from app.tools.function_tools import (
    read_function,
)


class EntityExtractor:

    def extract(
        self,
        question: str,
    ):

        q = question.strip()

        words = q.split()

        for word in words:

            function = read_function(
                word
            )

            if function:

                intent = self._detect_intent(
                    q.lower()
                )

                return {
                    "kind": "function",
                    "value": word,
                    "intent": intent,
                }

        return {
            "kind": "topic",
            "value": q,
            "intent": self._detect_intent(
                q.lower()
            ),
        }

    def _detect_intent(
        self,
        question: str,
    ):

        if "trace" in question:

            return "trace"

        if "explain" in question:

            return "explain"

        if "security" in question:

            return "security"

        if (
            "architecture" in question
            or "flow" in question
            or "how does" in question
        ):

            return "architecture"

        return "rag"