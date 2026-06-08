from app.retrieval.embeddings import embed

vector = embed(
    "How does middleware work?"
)

print(len(vector))