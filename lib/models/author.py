import sqlite3

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def all(cls):
        conn = sqlite3.connect('lib/db/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        authors = [cls(id=row[0], name=row[1]) for row in rows]
        conn.close()
        return authors

    def articles(self):
        from lib.models.article import Article  # moved inside method
        conn = sqlite3.connect('lib/db/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine  # moved inside method
        conn = sqlite3.connect('lib/db/database.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]
        