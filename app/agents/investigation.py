class Investigation:

    def __init__(
        self,
        question: str,
        target: str,
    ):
        self.question = question
        self.target = target

        self.trace = None
        self.architecture = None
        self.security = None

        self.notes = []