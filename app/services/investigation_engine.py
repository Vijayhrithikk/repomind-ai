class InvestigationEngine:

    def next_steps(
        self,
        hypotheses,
    ):

        steps = []

        texts = [
            item["hypothesis"].lower()
            for item in hypotheses
        ]

        if (
            "database may become a scalability bottleneck during traffic spikes"
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
            "cache hit rate is critical to system performance"
            in texts
        ):

            steps.append(
                {
                    "tool": "architecture",
                    "target": "cache",
                    "reason": "Validate cache effectiveness",
                }
            )

        if (
            "analytics failures should not impact redirect latency"
            in texts
        ):

            steps.append(
                {
                    "tool": "architecture",
                    "target": "analytics",
                    "reason": "Validate analytics isolation",
                }
            )

        return steps