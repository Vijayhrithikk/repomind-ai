class RiskAnalyzer:

    def analyze(
        self,
        architecture,
        scalability,
    ):

        risks = []

        architecture_text = str(
            architecture
        ).lower()

        scalability_text = str(
            scalability
        ).lower()

        if (
            "database dependency detected"
            in scalability_text
        ):

            risks.append(
                "Single database dependency may become a bottleneck under high traffic"
            )

        if (
            "potential database bottleneck"
            in scalability_text
        ):

            risks.append(
                "Database scaling strategy should be reviewed"
            )

        if (
            "cache-aside pattern detected"
            in architecture_text
        ):

            risks.append(
                "Caching reduces database read pressure"
            )

        if (
            "asynchronous processing detected"
            in architecture_text
        ):

            risks.append(
                "Background jobs are isolated from request latency"
            )

        return risks