from pgvector.psycopg import register_vector
from pgvector.psycopg import Vector

from app.db.database import conn
from app.retrieval.embeddings import embed

register_vector(conn)


def search(
    question: str,
    limit: int = 5,
):

    query_embedding = Vector(embed(question))

    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                function_name,
                file_path,
                content,
                embedding <=> %s AS distance
            FROM function_chunks
            ORDER BY distance
            LIMIT %s
            """,
            (
                query_embedding,
                limit,
            ),
        )

        return cur.fetchall()