class HypothesisGenerator:

    def generate(
        self,
        findings,
    ):

        hypotheses = []

        finding_text = str(
            findings
        ).lower()

        if (
            "database is a critical dependency"
            in finding_text
        ):

            hypotheses.append(
                {
                    "hypothesis":
                    "Database may become a scalability bottleneck during traffic spikes",

                    "confidence": 0.85,
                }
            )

        if (
            "caching reduces read pressure"
            in finding_text
        ):

            hypotheses.append(
                {
                    "hypothesis":
                    "Cache hit rate is critical to system performance",

                    "confidence": 0.80,
                }
            )

        if (
            "background processing reduces impact on request latency"
            in finding_text
        ):

            hypotheses.append(
                {
                    "hypothesis":
                    "Analytics failures should not impact redirect latency",

                    "confidence": 0.75,
                }
            )

        return hypotheses