from fastapi import FastAPI

from app.api.routes import router
from app.retrieval.embeddings import embed

app = FastAPI(
    title="RepoMind AI",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
def root():
    return{
        "message":"RepoMind AI is running"
    }

