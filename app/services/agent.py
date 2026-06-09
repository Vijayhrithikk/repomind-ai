from app.services.rag_service import RAGService
from app.services.trace_service import TraceService
from app.services.explain_service import ExplainService
from app.services.compare_service import CompareService
from app.services.security_review import (
    SecurityReviewService,
)
from app.services.repository_summary import (
    RepositorySummaryService,
)
from app.services.repository_explorer import (
    RepositoryExplorer,
)


class AgentService:

    def __init__(self):

        self.rag = RAGService()
        self.trace = TraceService()
        self.explain = ExplainService()
        self.compare = CompareService()
        self.security = SecurityReviewService()

        self.summary = RepositorySummaryService()

        self.explorer = RepositoryExplorer()

    def run(
        self,
        question: str,
    ):

        q = question.lower()

        if "security" in q:

            return {
                "tool": "security_review",
                "result": self.security.review(),
            }

        if "trace" in q:

            function_name = (
                question
                .replace("trace", "")
                .strip()
            )

            return {
                "tool": "trace",
                "result": self.trace.deep_trace(
                    function_name
                ),
            }

        if "explain" in q:

            function_name = (
                question
                .replace("explain", "")
                .strip()
            )

            return {
                "tool": "explain",
                "result": self.explain.explain(
                    function_name
                ),
            }

        if "summary" in q:

            investigation = (
                self.explorer.investigate(
                    "architecture"
                )
            )

            return {
                "tool": "summary",
                "result": self.summary.summarize(
                    investigation["functions"]
                ),
            }

        return {
            "tool": "rag",
            "result": self.rag.ask(
                question
            ),
        }