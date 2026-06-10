from app.services.repository_explorer import (
    RepositoryExplorer,
)


class ArchitectureReviewService:

    def __init__(self):

        self.explorer = RepositoryExplorer()

    def review(
        self,
        target: str,
    ):

        investigation = (
            self.explorer.investigate(
                target
            )
        )

        functions = (
            investigation["functions"]
        )

        layers = {
            "handlers": [],
            "services": [],
            "repositories": [],
        }

        for function in functions:

            path = (
                function["file_path"]
                .replace("\\", "/")
                .lower()
            )

            if "/handlers/" in path:

                layers["handlers"].append(
                    function["function_name"]
                )

            elif "/services/" in path:

                layers["services"].append(
                    function["function_name"]
                )

            elif "/repositories/" in path:

                layers["repositories"].append(
                    function["function_name"]
                )

        return {
            "layers": layers,
            "functions": functions,
        }