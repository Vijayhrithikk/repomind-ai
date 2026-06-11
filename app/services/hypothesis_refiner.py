class HypothesisRefiner:

    def refine(
        self,
        hypotheses,
        followups,
    ):

        refined = []

        for hypothesis in hypotheses:

            text = (
                hypothesis["hypothesis"]
                .lower()
            )

            if (
                "database"
                in text
            ):

                for item in followups:

                    result = str(
                        item["result"]
                    ).lower()

                    if (
                        "redis"
                        in result
                    ):

                        refined.append(
                            {
                                "hypothesis":
                                "Database read bottleneck risk reduced due to Redis caching",

                                "confidence":
                                0.75,
                            }
                        )

                        break

                else:

                    refined.append(hypothesis)

            else:

                refined.append(hypothesis)

        return refined