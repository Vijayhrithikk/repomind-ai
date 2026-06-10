class Evidence:

    def __init__(self):

        self.observations = []
        self.unknowns = []

    def add_observation(
        self,
        observation: str,
    ):
        self.observations.append(observation)

    def add_unknown(
        self,
        unknown: str,
    ):
        self.unknowns.append(unknown)