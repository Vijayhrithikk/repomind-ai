from app.services.repository_explorer import (
    RepositoryExplorer,
)
from app.services.system_mapper import (
    SystemMapper,
)
from app.services.flow_analyzer import FlowAnalyzer
from app.services.end_to_end_flow import EndToEndFlowService
from app.services.flow_cleaner import FlowCleaner


class ArchitectureReviewService:

    def __init__(self):

        self.explorer = RepositoryExplorer()
        self.mapper = SystemMapper()
        self.flow_analyzer = FlowAnalyzer()
        self.end_to_end= EndToEndFlowService()
        self.cleaner = FlowCleaner()

    def review(
        self,
        target: str,
    ):

        investigation = (self.explorer.investigate(target))

        functions = (investigation["functions"])
        print(type(functions))
        print(len(functions))

        systems = self.mapper.map_systems(functions)

        relationships = (investigation["relationships"])

        flows = self.flow_analyzer.analyze(relationships)
        flows = self.cleaner.clean(flows)

        workflows = self.end_to_end.analyze(
            {
                "systems":systems ,
                "flows": flows,
            }
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

                layers["handlers"].append(function["function_name"])

            elif "/services/" in path:

                layers["services"].append(function["function_name"])

            elif "/repositories/" in path:

                layers["repositories"].append(function["function_name"])

        entrypoints = (self._detect_entrypoints(functions))

        flows = (self._detect_flows(relationships))

        dependencies = (self._detect_dependencies(functions))

        return {
            "systems": systems,
            "workflows": workflows,
            "layers": layers,
            "entrypoints": entrypoints,
            "flows": flows,
            "dependencies": dependencies,
            "functions": functions,
        }

    def _detect_entrypoints(
        self,
        functions,
    ):

        entrypoints = []

        for function in functions:

            name = (
                function["function_name"]
            )

            path = (
                function["file_path"]
                .replace("\\", "/")
                .lower()
            )

            if (
                "/handlers/" in path
                or "handler" in name.lower()
                or name == "main"
            ):

                entrypoints.append(
                    name
                )

        return entrypoints

    def _detect_flows(
        self,
        relationships,
    ):

        flows = []

        for caller, callees in relationships.items():

            if not callees:
                continue

            flows.append(
                {
                    "from": caller,
                    "to": callees,
                }
            )

        return flows

    def _detect_dependencies(
        self,
        functions,
    ):

        dependencies = set()

        for function in functions:

            content = (
                function["content"]
                .lower()
            )

            if "jwt" in content:

                dependencies.add(
                    "JWT"
                )

            if "redis" or "setcache" in content:

                dependencies.add(
                    "Redis"
                )

            if "bcrypt" in content:

                dependencies.add(
                    "Bcrypt"
                )

            if (
                "postgres" in content
                or "pgx" in content
                or "sql" in content
            ):

                dependencies.add(
                    "PostgreSQL"
                )
            if "pushanalyticsjob" in content:
                dependencies.add("Analytics Queue")

        return list(
            dependencies
        )