from app.retrieval.embeddings import embed
from app.retrieval.repository import (
    FunctionRepository,
)
from app.graph.extractor import (
    extract_calls,
)

from app.graph.repository import (
    GraphRepository,
)

repo = FunctionRepository()


def index_functions(chunks):
    graph_repo = GraphRepository()
    total = len(chunks)

    for idx, chunk in enumerate(chunks):

        text_for_embedding = f"""
        Function Name:
        {chunk.function_name}

        Source Code:

        {chunk.content}
        """

        vector = embed(text_for_embedding)

        repo.save(
            chunk.file_path,
            chunk.function_name,
            chunk.content,
            vector,
        )
        calls = extract_calls(
            chunk.function_name,
            chunk.content,
        )

        for caller, callee in calls:
            graph_repo.save_edge(
                caller,
                callee,
            )

        print(
            f"[{idx+1}/{total}] "
            f"{chunk.function_name}"
        )