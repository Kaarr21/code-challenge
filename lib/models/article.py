import sqlite3
from lib.db.connection import get_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    def author(self):
        from lib.models.author import Author  # ✅ Lazy import inside method
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        conn.close()
        return Author(*row) if row else None

    def magazine(self):
        from lib.models.magazine import Magazine  # ✅ Lazy import inside method
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return Magazine(*row) if row else None
        