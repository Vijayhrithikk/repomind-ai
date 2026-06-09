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
    
    def deep_trace(self,function_name: str,depth: int = 2):
        visited = set()

        def dfs(
            current_function: str,
            current_depth: int,
        ):

            if current_depth > depth:
                return {}

            if current_function in visited:
                return {}

            visited.add(
                current_function
            )

            children = self.graph.get_calls(
                current_function
            )

            result = {}

            for child in children:

                result[child] = dfs(
                    child,
                    current_depth + 1,
                )

            return result

        return {
            function_name: dfs(
                function_name,
                0,
            )
        }