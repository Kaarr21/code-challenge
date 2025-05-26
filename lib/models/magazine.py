# lib/models/magazine.py

from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name} ({self.category})>"

    @classmethod
    def create(cls, name, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (name, category)
        )
        conn.commit()
        magazine_id = cursor.lastrowid
        return cls(name, category, id=magazine_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], id=row[0])
        return None

    def articles(self):
        """Returns list of all articles published in the magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles 
            WHERE magazine_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def contributors(self):
        """Returns unique list of authors who have written for this magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def article_titles(self):
        """Returns list of titles of all articles in the magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles 
            WHERE magazine_id = ?
        """, (self.id,))
        return [row[0] for row in cursor.fetchall()]

    def contributing_authors(self):
        """Returns list of authors with more than 2 articles in the magazine"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(*) > 2
        """, (self.id,))
        return cursor.fetchall()

    @classmethod
    def top_publisher(cls):
        """Find the magazine with the most articles"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(a.id) as article_count 
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], id=row[0])
        return None

    def update(self, name=None, category=None):
        if name:
            self.name = name
        if category:
            self.category = category

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE magazines
            SET name = ?, category = ?
            WHERE id = ?
        """
        cursor.execute(sql, (self.name, self.category, self.id))
        conn.commit()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM magazines WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
