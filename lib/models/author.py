import sqlite3
from lib.db.connection import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def save(self):
        """Save the author to the database"""
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def create(cls, name):
        """Create and save a new author"""
        author = cls(None, name)
        return author.save()

    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Find an author by name"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    def articles(self):
        """Returns list of all articles written by the author"""
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(*row) for row in rows]

    def magazines(self):
        """Returns unique list of magazines the author has contributed to"""
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(*row) for row in rows]

    def add_article(self, magazine, title):
        """Creates and inserts a new Article into the database"""
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (title, "", self.id, magazine.id)
        )
        article_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Article(article_id, title, "", self.id, magazine.id)

    def topic_areas(self):
        """Returns unique list of categories of magazines the author has contributed to"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.category
            FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    @classmethod
    def most_articles(cls):
        """Find the author who has written the most articles"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            LEFT JOIN articles ON authors.id = articles.author_id
            GROUP BY authors.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        return cls(row[0], row[1]) if row else None

    def __repr__(self):
        return f"<Author {self.name}>"
        