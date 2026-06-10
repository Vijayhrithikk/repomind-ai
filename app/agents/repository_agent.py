from app.agents.planner import Planner
from app.agents.synthesizer import Synthesizer
from app.agents.entity_extractor import (
    EntityExtractor,
)
from app.agents.investigation import (
    Investigation,
)
from app.agents.tool_executer import (
    ToolExecutor,
)


class RepositoryAgent:

    def __init__(self):

        self.planner = Planner()

        self.synthesizer = Synthesizer()

        self.extractor = EntityExtractor()

        self.executor = ToolExecutor()

    def run(
        self,
        question: str,
    ):

        entity = self.extractor.extract(question)

        plan = self.planner.plan(question,entity,)

        print(
            "Intent",
            entity.get("intent"),
        )

        print(
            "Entity:",
            entity,
        )

        target = (
            entity.get("value")
            or question
        )

        investigation = Investigation(
            question=question,
            target=target,
        )

        results = {}

        for tool in plan["tools"]:

            result = self.executor.execute(
                tool=tool,
                target=target,
                question=question,
                investigation=investigation,
                collect_trace_observations=self._collect_trace_observations,
            )

            if result is not None:

                results[tool] = result

        answer = (
            self.synthesizer.synthesize(
                question,
                results,
                investigation.notes,
                investigation.evidence,
            )
        )

        return {
            "plan": plan,
            "answer": answer,
            "tool_results": results,
            "evidence": {
                "observations": (
                    investigation.evidence.observations
                ),
                "unknowns": (
                    investigation.evidence.unknowns
                ),
            },
        }

    def _collect_trace_observations(
        self,
        tree: dict,
        evidence,
    ):

        for caller, children in tree.items():

            if isinstance(children,dict):

                for callee in children.keys():

                    evidence.add_observation(
                        f"{caller} calls {callee}",
                        source="trace",
                        confidence=1.0,
                    )

                    self._collect_trace_observations(
                        {
                            callee:
                            children[callee]
                        },
                        evidence,
                    )