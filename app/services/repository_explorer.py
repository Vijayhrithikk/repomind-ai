from app.retrieval.search import search
from app.tools.function_tools import read_function


class RepositoryExplorer:

    def investigate(
        self,
        query: str,
    ):

        results = search(
            query,
            limit=5,
        )

        findings = []

        for result in results:

            function_name = result[0]

            function = read_function(
                function_name
            )

            if function:
                findings.append(
                    function
                )

        return {
                "functions": findings,
                "sources": [f["function_name"] for f in findings]
                }