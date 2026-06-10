class Evidence:

    def __init__(self):

        self.observations = []
        self.unknowns = []

    def add_observation(
        self,
        observation: str,
        source: str = "unknown",
        confidence: float=1.0,
    ):

        self.observations.append(
            {
                "fact": observation,
                "source": source,
                "confidence":1.0,
            }
        )

    def add_unknown(
        self,
        unknown: str,
        source: str = "unknown",
    ):

        self.unknowns.append(
            {
                "fact": unknown,
                "source": source,
            }
        )