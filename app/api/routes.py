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


@router.get("/test")
def test():
    ans = gemini.generate("Explain Redis in one sentence")

    return {
        "answer": ans
    }

@router.get("/repo/load")
def load_repo():
    repo_path= repo_service.clone_repo("https://github.com/Vijayhrithikk/shortly")

    files= repo_service.get_go_files(repo_path)

    return {
        "files": len(files)
    }


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