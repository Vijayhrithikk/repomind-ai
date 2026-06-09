from app.retrieval.search import search
from app.retrieval.keyword_search import (
    keyword_search,
)


def hybrid_search(
    query: str,
    limit: int = 5,
):

    vector_results = search(query,limit,)

    keyword_results = keyword_search(query,limit)

    combined = []

    seen = set()

    for row in vector_results:

        name = row[0]

        if name in seen:
            continue

        seen.add(name)

        combined.append(row)

    for row in keyword_results:

        name = row[0]

        if name in seen:
            continue

        seen.add(name)

        combined.append(row)

    return combined[:limit]