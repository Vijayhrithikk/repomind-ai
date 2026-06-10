from fastapi import APIRouter

from app.core.gemini import GeminiClient
from app.services.repo_service import RepoService
from app.indexing.parser import extract_functions
from app.retrieval.indexer import index_functions
from app.retrieval.search import search
from app.tools.function_tools import read_function
from app.services.repository_explorer import RepositoryExplorer
from app.services.rag_service import RAGService

router = APIRouter()

gemini = GeminiClient()
repo_service= RepoService()

#test gemini api
@router.get("/test")
def test():
    ans = gemini.generate("Explain Redis in one sentence")

    return {
        "answer": ans
    }

#test repo clone
@router.get("/repo/load")
def load_repo():
    repo_path= repo_service.clone_repo("https://github.com/Vijayhrithikk/shortly")

    files= repo_service.get_go_files(repo_path)

    return {
        "files": len(files)
    }

#test repo clone and chunk
@router.post("/repo/functions")
def repo_functions():

    repo_path = repo_service.clone_repo(
        "https://github.com/gin-gonic/gin"
    )

    files = repo_service.get_go_files(repo_path)
    

    chunks = []

    for file in files:
        
        chunks.extend(extract_functions(str(file)))

    return {
        "functions": len(chunks),
        "examples": [
            c.function_name
            for c in chunks[:10]
        ]
    }

#test repo retrieval,embed and save
@router.post("/repo/index")
def repo_index():
    repo_path = repo_service.clone_repo(
        "https://github.com/Vijayhrithikk/shortly"
    )

    files = repo_service.get_go_files(repo_path)
    

    chunks = []

    for file in files:

        if file.name.endswith("_test.go"):
            continue

        chunks.extend(extract_functions(str(file)))
    index_functions(chunks)

# test search
@router.get("/search")
def semantic_search(q: str):
    results = search(q)

    return [
        {
            "function": r[0],
            "file": r[1],
            "distance": r[3],
        }
        for r in results
    ]


@router.get("/function")
def get_function(
    name: str
):
    return read_function(name)

explorer = RepositoryExplorer()


@router.get("/investigate")
def investigate(
    q: str
):
    return explorer.investigate(q)

rag_service = RAGService()


@router.get("/ask")
def ask(q: str):
    return rag_service.ask(q)

    
#summarize tool
from app.services.repository_summary import (
    RepositorySummaryService,
)

summary_service = RepositorySummaryService()

@router.get("/summary")
def summary():

    investigation = explorer.investigate(
        "application architecture"
    )

    return {
        "summary": summary_service.summarize(
            investigation["functions"]
        )
    }

#trace service
from app.services.trace_service import (
    TraceService,
)

trace_service = TraceService()

@router.get("/trace")
def trace(
    q: str
):
    return trace_service.trace(q)

#deep trace
@router.get("/trace/deep")
def deep_trace(
    name: str
):
    return trace_service.deep_trace(
        name
    )

#explain service 

from app.services.explain_service import (
    ExplainService,
)
explain_service = ExplainService()

@router.get("/explain")
def explain(
    name: str
):
    return explain_service.explain(
        name
    )

#comparison
from app.services.compare_service import (
    CompareService,
)

compare_service = CompareService()
@router.get("/compare")
def compare(
    func1: str,
    func2: str,
):
    return compare_service.compare(
        func1,
        func2,
    )

#security_pr
from app.services.security_review import (
    SecurityReviewService,
)

security_service = SecurityReviewService()

@router.get("/security-review")
def security_review():
    return {
        "review": security_service.review()
    }



#agents 

from app.agents.repository_agent import (
    RepositoryAgent,
)

repository_agent = RepositoryAgent()

@router.get("/agent")
def agent(q: str):
    return repository_agent.run(q)

#test synthesizer

from app.agents.synthesizer import Synthesizer
s = Synthesizer()
@router.get("/syn")
def planners():
    return s.synthesize(

        "How secure is authentication?",
        {
            "trace": "Login -> GetUserByEmail",
            "security_review": "Missing rate limiting",
        },
        )   
    
#test keyword
from app.retrieval.hybrid_search import hybrid_search

@router.get("/hybrid")
def keyword():
    return {
        "ans": hybrid_search("Login")
    }

#test entity extractor
from app.agents.entity_extractor import EntityExtractor

entity = EntityExtractor()

@router.get("/en")
def extractor():
    return {
        "ans": entity.extract("How secure is authentication")
    }