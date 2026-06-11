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
from app.services.investigation_engine import InvestigationEngine

from app.services.evidence_fusion import EvidenceFusion

from app.services.hypothesis_generator import HypothesisGenerator

from app.services.hypothesis_refiner import HypothesisRefiner

from app.services.question_planner import QuestionPlanner


class RepositoryAgent:

    def __init__(self):

        self.planner = Planner()

        self.synthesizer = Synthesizer()

        self.extractor = EntityExtractor()

        self.executor = ToolExecutor()

        self.tool_executor = ToolExecutor()

        self.investigation_engine = InvestigationEngine()

        self.fusion = EvidenceFusion()

        self.hypothesis_generator = HypothesisGenerator()

        self.hypothesis_refiner = HypothesisRefiner()

        self.question_planner = QuestionPlanner()

    def run(
        self,
        question: str,
    ):
        import time 

        start =time.time()

        entity = self.extractor.extract(question)

        print("entity extract:",time.time()-start)
        start = time.time()

        plan = self.planner.plan(question,entity,)
        print("Planner:",time.time()-start)

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

        start = time.time()
        investigation = Investigation(
            question=question,
            target=target,
        )
        print("Investigate:",time.time()-start)

        results = {}
        start = time.time()
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

        print("Architecture:",time.time()-start)

        

        investigation.findings = self.fusion.fuse(investigation.evidence)

        investigation.hypotheses = self.hypothesis_generator.generate(investigation.findings)

        next_steps = self.investigation_engine.next_steps(investigation.hypotheses)

        followups = []

        if next_steps:

            first_step = next_steps[0]

            result = self.tool_executor.execute(
                tool=first_step["tool"],
                target=first_step["target"],
                question=question,
                investigation=investigation,
                collect_trace_observations=self._collect_trace_observations,
            )
            investigation.investigated_targets.add(first_step["target"])

            followups.append(
                {
                    "step": first_step,
                    "result": result,
                }
            )     

        investigation.refined_hypotheses = self.hypothesis_refiner.refine(investigation.hypotheses,followups) 

        questions = []

        for hypothesis in investigation.refined_hypotheses:

            text = hypothesis["hypothesis"].lower()

            if "redis" in text:

                questions.append(
                    "Can Redis outage affect redirect latency?"
                )

            if "cache" in text:

                questions.append(
                    "How is cache invalidation handled?"
                )

            if "analytics" in text:

                questions.append(
                    "Can analytics queue backlog impact performance?"
                )

        investigation.open_questions = questions

        question_steps = self.question_planner.plan(investigation.open_questions)

        second_round_steps = self.investigation_engine.next_steps(investigation.refined_hypotheses)  

        second_followups = []

        if second_round_steps:

            first_step = second_round_steps[0]

            result = self.tool_executor.execute(
                tool=first_step["tool"],
                target=first_step["target"],
                question=question,
                investigation=investigation,
                collect_trace_observations=self._collect_trace_observations,
            )
            investigation.investigated_targets.add(first_step["target"])

            second_followups.append(
                {
                    "step": first_step,
                    "result": result,
                }
            )

        start= time.time()
        answer = (
            self.synthesizer.synthesize(
                question,
                results,
                investigation.notes,
                investigation.evidence,
            )
        )
        print("Synthesizer:",time.time()-start)

        return {
            "plan": plan,
            "answer": answer,
            "tool_results": results,
            "findings": investigation.findings,
            "hypotheses": investigation.hypotheses,
            "followups": followups,
            "next_steps": next_steps,
            "refined_hypotheses": investigation.refined_hypotheses,
            "second_round_steps": second_round_steps,
            'second_followups': second_followups,
            "investigated_targets": list(investigation.investigated_targets),
            "open_questions": investigation.open_questions,
            "question_steps": question_steps,
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