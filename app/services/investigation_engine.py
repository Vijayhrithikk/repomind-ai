class InvestigationEngine:

    def next_steps(
        self,
        evidence,
    ):

        steps = []

        observations = (evidence.observations)

        facts = [
            item["fact"].lower()
            for item in observations
        ]

        if (
            "database dependency detected"
            in facts
        ):

            steps.append(
                {
                    "tool": "architecture",
                    "target": "database",
                    "reason": "Investigate database dependency",
                }
            )

        if (
            "cache-aside pattern detected"
            in facts
        ):

            steps.append(
                {
                    "tool": "architecture",
                    "target": "cache",
                    "reason": "Investigate cache architecture",
                }
            )

        return steps