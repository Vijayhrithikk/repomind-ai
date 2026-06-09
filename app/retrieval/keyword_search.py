from app.db.database import conn


def keyword_search(
    query: str,
    limit: int = 5,
):

    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                function_name,
                file_path,
                content,
                0.0 AS score
            FROM function_chunks
            WHERE
                function_name ILIKE %s
                OR
                content ILIKE %s
            LIMIT %s
            """,
            (
                f"%{query}%",
                f"%{query}%",
                limit,
            ),
        )

        return cur.fetchall()