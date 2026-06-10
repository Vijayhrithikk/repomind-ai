from app.tools.function_tools import read_function
from app.graph.repository import GraphRepository
from app.retrieval.hybrid_search import hybrid_search


class RepositoryExplorer:

    def __init__(self):
        self.graph = GraphRepository()

    def investigate(
        self,
        query: str,
    ):

        results = hybrid_search(
            query,
            limit=10,
        )

        findings = []
        seen = set()

        relationships = {}

        for result in results:

            function_name = result[0]

            function = read_function(
                function_name
            )

            if (
                function
                and function["function_name"] not in seen
            ):

                findings.append(function)

                seen.add(
                    function["function_name"]
                )

            related_functions = self.graph.get_calls(function_name)

            relationships[
                function_name
            ] = related_functions

            for callee in related_functions:

                related_function = read_function(callee)

                if (
                    related_function
                    and related_function["function_name"] not in seen
                ):

                    findings.append(related_function)

                    seen.add(related_function["function_name"])

        print(
            [
                f["function_name"]
                for f in findings
            ]
        )

        return {
            "functions": findings,
            "sources": [
                f["function_name"]
                for f in findings
            ],
            "relationships": relationships,
        }