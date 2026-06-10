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

        

        entity = self.extractor.extract(question)
        plan = self.planner.plan(question,entity)

        intent = entity.get("intent")
        print("Intent",intent)

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

                investigation.add_note(f"Trace completed for {target}")

            elif tool == "explain":

                investigation.explain = (explain_tool.explain(target))

                results["explain"] = (investigation.explain)
                investigation.add_note(f"Function Explanation generated for {target}")

            elif tool == "security_review":

                investigation.security = (security_tool.review(target))

                results["security_review"] = (investigation.security)
                investigation.add_note(f"Security review completed for {target}")

            elif tool == "rag":

                investigation.rag = (rag_tool.ask(question))

                results["rag"] = (investigation.rag)
                investigation.add_note(f"Rag question completed for {target}")


            elif tool == "architecture":

                investigation.architecture = (architecture_tool.review(target))

                results["architecture"] = (investigation.architecture)
                investigation.add_note(f"Architecture analyzed for {target}")

        answer = (
            self.synthesizer.synthesize(
                question,
                results,
                investigation.notes,
            )
        )

        return {
            "plan": plan,
            "answer": answer,
            "tool_results": results,
        }