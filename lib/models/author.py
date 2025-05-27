import sqlite3
from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @staticmethod
    def find_by_id(author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Author(id=row['id'], name=row['name'])
        return None

    @staticmethod
    def find_by_name(name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Author(id=row['id'], name=row['name'])
        return None

    @staticmethod
    def all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        conn.close()
        return [Author(id=row['id'], name=row['name']) for row in rows]

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(id=row['id'], name=row['name'], category=row['category']) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['category'] for row in rows]

    @staticmethod
    def most_prolific():
        """Find the author who has written the most articles"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, COUNT(art.id) as article_count 
            FROM authors a
            JOIN articles art ON a.id = art.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        ''')
        row = cursor.fetchone()
        conn.close()
        if row:
            return Author(id=row['id'], name=row['name'])
        return None

    def __repr__(self):
        return f"<Author {self.name}>"
        