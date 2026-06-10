class Investigation:

    def __init__(
        self,
        question: str,
        target: str,):
        
        self.question = question
        self.target = target

        self.trace = None
        self.explain = None
        self.architecture = None
        self.security = None
        self.rag = None

        self.notes = []

    def add_note(self,note: str,):
        self.notes.append(note)