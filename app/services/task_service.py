from app.services.db import get_connection


def get_all_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, is_done FROM tasks ORDER BY id")
            return cur.fetchall()


def get_unfinished_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, is_done FROM tasks WHERE is_done = FALSE ORDER BY id"
            )
            return cur.fetchall()


def create_task(title):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, is_done",
                (title,),
            )
            task = cur.fetchone()
        conn.commit()
    return task


def toggle_task_status(task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, is_done FROM tasks WHERE id = %s", (task_id,))
            task = cur.fetchone()
            if not task:
                return None

            new_status = not task["is_done"]
            cur.execute(
                """
                UPDATE tasks
                SET is_done = %s
                WHERE id = %s
                RETURNING id, title, is_done
                """,
                (new_status, task_id),
            )
            updated_task = cur.fetchone()
        conn.commit()
    return updated_task


def delete_task_by_id(task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            deleted = cur.rowcount > 0
        conn.commit()
    return deleted
