from app.db.database import conn


class GraphRepository:

    def save_edge(
        self,
        caller: str,
        callee: str,
    ):

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO function_calls(
                    caller,
                    callee
                )
                VALUES (%s, %s)
                """,
                (
                    caller,
                    callee,
                )
            )

        conn.commit()

    def get_calls(
        self,
        function_name: str,
    ):

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT callee
                FROM function_calls
                WHERE caller = %s
                """,
                (
                    function_name,
                )
            )

            return [
                row[0]
                for row in cur.fetchall()
            ]