from app.db.database import conn


def read_function(function_name: str):

    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT
                function_name,
                file_path,
                content
            FROM function_chunks
            WHERE function_name = %s
            LIMIT 1
            """,
            (function_name,)
        )

        row = cur.fetchone()

        if not row:
            return None

        return {
            "function_name": row[0],
            "file_path": row[1],
            "content": row[2],
        }