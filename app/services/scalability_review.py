class ScalabilityReviewService:

    def review(
        self,
        architecture,
    ):

        findings = []

        flows = architecture.get(
            "flows",
            []
        )

        flow_text = str(
            flows
        ).lower()

        if ("queryrow"
            in flow_text):

            findings.append("Database dependency detected")

        if (
            "comparehashandpassword"
            in flow_text
        ):

            findings.append("CPU intensive authentication flow")

        if (
            "getcache"
            not in flow_text
            and "queryrow"
            in flow_text
        ):

            findings.append("Potential database bottleneck")

        if (
            "pushanalyticsjob"
            in flow_text
        ):

            findings.append("Asynchronous processing improves scalability")

        return findings