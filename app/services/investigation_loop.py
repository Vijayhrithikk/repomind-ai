class InvestigationLoop:

    def run(
        self,
        next_steps,
    ):

        if not next_steps:
            return []

        return [next_steps[0]]