from app.agents.evidence import Evidence
class Investigation:

    def __init__(
        self,
        question: str,
        target: str,):
        
        self.question = question
        self.target = target

        self.trace = None
        self.risks = None
        self.explain = None
        self.architecture = None
        self.security = None
        self.scalability = None
        self.rag = None

        self.findings = []
        self.hypotheses = []
        self.refined_hypotheses = []
        self.notes = []
        self.investigated_targets = set()
        self.open_questions = []
        self.evidence = Evidence()

    def add_note(self,note: str,):
        self.notes.append(note)