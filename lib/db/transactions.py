import sqlite3
from lib.db.connection import get_connection

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction.
    articles_data: list of dicts with 'title' and 'magazine_id' keys.
    """
    conn = get_connection()

    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO authors (name) VALUES (?) RETURNING id",
            (author_name,)
        )
        author_id = cursor.fetchone()[0]

        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article["title"], author_id, article["magazine_id"])
            )

        conn.execute("COMMIT")
        print("Transaction successful.")
        return True

    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return False

    finally:
        conn.close()
