from app.agents.tools import (
    trace_tool,
    explain_tool,
    security_tool,
    rag_tool,
)


class RepositoryAgent:

    def run(
        self,
        question: str,
    ):

        q = question.lower()

        if (
            "security" in q
            and
            "authentication" in q
        ):

            trace = trace_tool.deep_trace("Login")

            explanation = (
                explain_tool.explain("Login")
            )

            review = (
                security_tool.review()
            )

            return {
                "workflow": [
                    "trace",
                    "explain",
                    "security_review",
                ],
                "trace": trace,
                "explanation": explanation,
                "security_review": review,
            }

        if "trace" in q:

            function_name = (question.replace("trace", "").strip())

            return {
                "workflow": ["trace",],
                "result": trace_tool.deep_trace(function_name),
            }

        if "explain" in q:

            function_name = (question.replace("explain", "").strip())

            return {
                "workflow": ["explain",],
                "result": explain_tool.explain(function_name),
            }

        return {
            "workflow": ["rag",],
            "result": rag_tool.ask(question),
        }