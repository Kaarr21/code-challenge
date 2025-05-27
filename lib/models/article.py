import sqlite3
from lib.db.connection import get_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        """Save the article to the database"""
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.content, self.author_id, self.magazine_id, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                (self.title, self.content, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        """Create and save a new article"""
        article = cls(None, title, content, author_id, magazine_id)
        return article.save()

    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def find_by_title(cls, title):
        """Find articles by title"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def find_by_author(cls, author_id):
        """Find articles by author ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        """Find articles by magazine ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    def author(self):
        """Get the author of this article"""
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        conn.close()
        return Author(*row) if row else None

    def magazine(self):
        """Get the magazine this article belongs to"""
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return Magazine(*row) if row else None

    def __repr__(self):
        return f"<Article {self.title}>"
        