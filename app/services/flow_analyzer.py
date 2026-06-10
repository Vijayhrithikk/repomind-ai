class FlowAnalyzer:

    def analyze(
        self,
        relationships,
    ):

        flows = []

        for caller, callees in relationships.items():

            if not callees:
                continue

            flows.append({
                "entrypoint": caller,
                "flow":callees,
            })

        return flows