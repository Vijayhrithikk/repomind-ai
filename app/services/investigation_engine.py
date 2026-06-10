class InvestigationEngine:

    def next_steps(
        self,
        hypotheses,
    ):

        steps = []

        observations = (hypotheses.observations)

        texts = [
            item["hypothesis"].lower()
            for item in hypotheses
        ]

        if (
            "database dependency detected"
            in texts
        ):

            steps.append(
                {
                    "tool": "architecture",
                    "target": "database",
                    "reason": "Validate database scalability hypothesis",
                }
            )

        if (
            "cache-aside pattern detected"
            in texts
        ):

            steps.append(
                {
                    "tool": "architecture",
                    "target": "cache",
                    "reason": "Validate cache-aside pattern hypothesis",
                }
            )

        return steps