class EvidenceFusion:

    def fuse(
        self,
        evidence,
    ):

        findings = []

        observations = [
            item["fact"].lower()
            for item in evidence.observations
        ]

        if (
            "database dependency detected"
            in observations
            and
            "potential database bottleneck"
            in observations
        ):

            findings.append(
                {
                    "finding":
                    "Database is a critical dependency and may become a bottleneck under load",
                    "confidence": 0.95,
                }
            )

        if (
            "cache-aside pattern detected"
            in observations
        ):

            findings.append(
                {
                    "finding":
                    "Caching reduces read pressure on the primary database",
                    "confidence": 0.90,
                }
            )

        if (
            "asynchronous processing detected"
            in observations
        ):

            findings.append(
                {
                    "finding":
                    "Background processing reduces impact on request latency",
                    "confidence": 0.90,
                }
            )

        return findings