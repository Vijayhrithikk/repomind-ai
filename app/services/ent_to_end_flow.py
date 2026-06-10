class EndToEndFlowService:

    def analyze(
        self,
        architecture,
    ):

        workflows = []

        systems = architecture.get(
            "systems",
            {},
        )

        flows = architecture.get(
            "flows",
            [],
        )

        for system_name, functions in systems.items():

            workflow = []

            for flow in flows:

                entrypoint = flow.get(
                    "entrypoint"
                )

                if (
                    entrypoint
                    in functions
                ):

                    workflow.append(
                        entrypoint
                    )

                    workflow.extend(
                        flow.get(
                            "flow",
                            []
                        )
                    )

            if workflow:

                workflows.append(
                    {
                        "system": system_name,
                        "steps": workflow,
                    }
                )

        return workflows