from pgvector.psycopg import register_vector

from app.db.database import conn

register_vector(conn)


class FunctionRepository:

    def save(self,
        file_path: str,
        function_name: str,
        content: str,
        embedding: list[float]):

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO function_chunks(
                    file_path,
                    function_name,
                    content,
                    embedding
                )
                VALUES (%s,%s,%s,%s)
                """,
                (
                    file_path,
                    function_name,
                    content,
                    embedding,
                ),
            )

        conn.commit()