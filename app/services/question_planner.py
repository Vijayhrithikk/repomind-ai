class QuestionPlanner:

    def plan(
        self,
        questions,
    ):

        steps = []

        for question in questions:

            q = question.lower()

            if "redis" in q:

                steps.append(
                    {
                        "tool": "architecture",
                        "target": "redis",
                        "reason": question,
                    }
                )

            elif "cache" in q:

                steps.append(
                    {
                        "tool": "architecture",
                        "target": "cache",
                        "reason": question,
                    }
                )

            elif "analytics" in q:

                steps.append(
                    {
                        "tool": "architecture",
                        "target": "analytics",
                        "reason": question,
                    }
                )

        return steps