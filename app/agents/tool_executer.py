from app.agents.evidence_extractors import (
    extract_trace_patterns,
    extract_architecture_patterns
)

from app.agents.tools import (
    trace_tool,
    explain_tool,
    security_tool,
    rag_tool,
    architecture_tool,
    scalability_tool
)


class ToolExecutor:

    def execute(
        self,
        tool: str,
        target: str,
        question: str,
        investigation,
        collect_trace_observations,
    ):

        if tool == "trace":

            investigation.trace = (
                trace_tool.deep_trace(target)
            )

            collect_trace_observations(
                investigation.trace,
                investigation.evidence,
            )

            semantic = (
                extract_trace_patterns(
                    investigation.evidence.observations
                )
            )

            for item in semantic:

                investigation.evidence.add_observation(
                    item,
                    source="trace",
                    confidence=0.90,
                )

            investigation.evidence.add_unknown(
                "Security properties not verified",
                source="trace",
                confidence=0.0,
            )

            investigation.add_note(
                f"Trace completed for {target}"
            )

            return investigation.trace

        elif tool == "explain":

            investigation.explain = (
                explain_tool.explain(target)
            )

            investigation.evidence.add_observation(
                f"Explanation generated for {target}",
                source="explain",
                confidence=1.0,
            )

            investigation.add_note(
                f"Function explanation generated for {target}"
            )

            return investigation.explain

        elif tool == "security_review":

            investigation.security = (
                security_tool.review(target)
            )

            investigation.evidence.add_observation(
                f"Security review executed for {target}",
                source="security_review",
                confidence=1.0,
            )

            investigation.add_note(
                f"Security review completed for {target}"
            )

            return investigation.security

        elif tool == "rag":

            investigation.rag = (
                rag_tool.ask(question)
            )

            investigation.add_note(
                f"RAG completed for {target}"
            )

            return investigation.rag
        
        elif tool == "scalability_review":

            investigation.scalability = (
                scalability_tool.review(
                    investigation.architecture
                )
            )

            for finding in (
                investigation.scalability
            ):

                investigation.evidence.add_observation(
                    finding,
                    source="scalability",
                    confidence=0.85,
                )

            investigation.add_note(
                f"Scalability review completed for {target}"
            )

            return investigation.scalability

        elif tool == "architecture":

            investigation.architecture = (
                architecture_tool.review(target)
            )
            patterns = extract_architecture_patterns(investigation.architecture)

            for pattern in patterns:
                investigation.evidence.add_observation(pattern,source="architecture",confidence=0.90)

            investigation.add_note(
                f"Architecture review executed for {target}"
            )

            investigation.add_note(
                f"Architecture analyzed for {target}"
            )

            return investigation.architecture

        return None