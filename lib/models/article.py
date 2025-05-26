from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"

    @classmethod
    def create(cls, title, author_id, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, author_id, magazine_id)
        )
        conn.commit()
        article_id = cursor.lastrowid
        return cls(title, author_id, magazine_id, id=article_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[3], id=row[0])
        return None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[3], id=row[0])
        return None

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        return [cls(row[1], row[2], row[3], id=row[0]) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        return [cls(row[1], row[2], row[3], id=row[0]) for row in rows]

    def author(self):
        """Returns the Author instance for this article"""
        return Author.find_by_id(self.author_id)

    def magazine(self):
        """Returns the Magazine instance for this article"""
        return Magazine.find_by_id(self.magazine_id)
