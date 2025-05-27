import sqlite3
from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        """Save the magazine to the database"""
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", 
                         (self.name, self.category, self.id))
        else:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", 
                         (self.name, self.category))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def create(cls, name, category):
        """Create and save a new magazine"""
        magazine = cls(None, name, category)
        return magazine.save()

    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Find a magazine by name"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def find_by_category(cls, category):
        """Find magazines by category"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    def articles(self):
        """Returns list of all articles published in the magazine"""
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(*row) for row in rows]

    def contributors(self):
        """Returns unique list of authors who have written for this magazine"""
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row) for row in rows]

    def article_titles(self):
        """Returns list of titles of all articles in the magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def contributing_authors(self):
        """Returns list of authors with more than 2 articles in the magazine"""
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row[0], row[1]) for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        """Find magazines with articles by at least 2 different authors"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.*, COUNT(DISTINCT articles.author_id) as author_count
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            HAVING author_count >= 2
        """)
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[0], row[1], row[2]) for row in rows]

    @classmethod
    def article_counts(cls):
        """Count the number of articles in each magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.name, COUNT(articles.id) as article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id, magazines.name
            ORDER BY article_count DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [(row[0], row[1]) for row in rows]

    @classmethod
    def top_publisher(cls):
        """BONUS: Find the magazine with the most articles"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.*, COUNT(articles.id) as article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        return cls(row[0], row[1], row[2]) if row else None

    def __repr__(self):
        return f"<Magazine {self.name} ({self.category})>"
        