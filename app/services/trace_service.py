from app.retrieval.search import search
from app.graph.repository import GraphRepository
from app.tools.function_tools import (
    read_function,
)


class TraceService:

    def __init__(self):
        self.graph = GraphRepository()

    def trace(
        self,
        query: str,
    ):

        function = read_function(
            query
        )

        if function:

            root = function["function_name"]

        else:

            results = search(
                query,
                limit=1,
            )

            if not results:
                return {}

            root = results[0][0]


        calls = self.graph.get_calls(
            root
        )

        return {
            "root": root,
            "calls": calls,
        }