import sqlite3
from lib.db.connection import get_connection

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction.
    articles_data: list of dicts with 'title', 'content', and 'magazine_id' keys.
    """
    conn = get_connection()

    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()

        # Insert author
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (author_name,)
        )
        author_id = cursor.lastrowid

        # Insert articles
        for article in articles_data:
            content = article.get('content', '')  # Default to empty string if no content
            cursor.execute(
                "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                (article["title"], content, author_id, article["magazine_id"])
            )

        conn.execute("COMMIT")
        print(f"Transaction successful. Author '{author_name}' added with {len(articles_data)} articles.")
        return True

    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return False

    finally:
        conn.close()

def bulk_insert_articles(articles_data):
    """
    Insert multiple articles in a single transaction.
    articles_data: list of dicts with 'title', 'content', 'author_id', and 'magazine_id' keys.
    """
    conn = get_connection()

    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()

        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                (article["title"], article.get("content", ""), article["author_id"], article["magazine_id"])
            )

        conn.execute("COMMIT")
        print(f"Successfully inserted {len(articles_data)} articles.")
        return True

    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Bulk insert failed: {e}")
        return False

    finally:
        conn.close()

def transfer_articles_between_magazines(old_magazine_id, new_magazine_id):
    """
    Transfer all articles from one magazine to another in a single transaction.
    """
    conn = get_connection()

    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()

        # Check if both magazines exist
        cursor.execute("SELECT COUNT(*) FROM magazines WHERE id IN (?, ?)", (old_magazine_id, new_magazine_id))
        if cursor.fetchone()[0] != 2:
            raise ValueError("One or both magazines do not exist")

        # Update articles
        cursor.execute(
            "UPDATE articles SET magazine_id = ? WHERE magazine_id = ?",
            (new_magazine_id, old_magazine_id)
        )
        
        affected_rows = cursor.rowcount
        conn.execute("COMMIT")
        print(f"Successfully transferred {affected_rows} articles from magazine {old_magazine_id} to {new_magazine_id}.")
        return True

    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transfer failed: {e}")
        return False

    finally:
        conn.close()
        