from app.agents.planner import Planner
from app.agents.synthesizer import Synthesizer
from app.agents.entity_extractor import (
    EntityExtractor,
)

from app.agents.tools import (
    trace_tool,
    explain_tool,
    security_tool,
    rag_tool,
    architecture_tool
)


class RepositoryAgent:

    def __init__(self):

        self.planner = Planner()

        self.synthesizer = Synthesizer()
        self.extractor= EntityExtractor()

    def run(
        self,
        question: str,
    ):

        plan = self.planner.plan(question)

        entity = self.extractor.extract(question)
        kind = entity.get("kind")
        value = entity.get("value")
        print("Entity:", entity)
        
        target = (value if value else question)

        results = {}

        for tool in plan["tools"]:

            if tool == "trace":

                results["trace"] = (
                    trace_tool.deep_trace(target)
                )

            elif tool == "explain":

                results["explain"] = (
                    explain_tool.explain(target)
                )

            elif tool == "security_review":
                

                results["security_review"] = (security_tool.review(target))

            elif tool == "rag":

                results["rag"] = (rag_tool.ask(question))
            elif tool == "architecture":
                results["architecture"] = architecture_tool.review(target)

        answer = (
            self.synthesizer.synthesize(
                question,
                results,
            )
        )

        return {
            "plan": plan,
            "answer": answer,
            "tool_results": results,
        }