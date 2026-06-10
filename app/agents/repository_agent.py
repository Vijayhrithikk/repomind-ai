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

        from app.agents.investigation import Investigation
    
        investigation = Investigation(
            question=question,
            target=target,
        )

        results = {}

        for tool in plan["tools"]:

            if tool == "trace":

                investigation.trace = (trace_tool.deep_trace(target))

                results["trace"] = (investigation.trace)

            elif tool == "explain":

                investigation.explain = (explain_tool.explain(target))

                results["explain"] = (investigation.explain)

            elif tool == "security_review":

                investigation.security = (security_tool.review(target))

                results["security_review"] = (investigation.security)

            elif tool == "rag":

                investigation.rag = (rag_tool.ask(question))

                results["rag"] = (investigation.rag)


            elif tool == "architecture":

                investigation.architecture = (architecture_tool.review(target))

                results["architecture"] = (investigation.architecture)

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