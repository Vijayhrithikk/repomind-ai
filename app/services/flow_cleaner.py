class FlowCleaner:

    NOISE = {
        "string",
        "error",
        "context",
        "ctx",
        "new",
        "group",
        "get",
        "post",
        "put",
        "delete",
        "json",
        "bind",
        "status",
    }

    def clean(
        self,
        flows,
    ):

        cleaned = []

        for flow in flows:

            steps = []

            for step in flow.get(
                "flow",
                [],
            ):

                name = step.lower()

                if name in self.NOISE:
                    continue

                steps.append(step)

            cleaned.append(
                {
                    "entrypoint": flow["entrypoint"],
                    "flow": steps,
                }
            )

        return cleaned