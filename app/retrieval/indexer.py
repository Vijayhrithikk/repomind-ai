from app.retrieval.embeddings import embed
from app.retrieval.repository import (
    FunctionRepository,
)


repo = FunctionRepository()


def index_functions(chunks):

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

        print(
            f"[{idx+1}/{total}] "
            f"{chunk.function_name}"
        )