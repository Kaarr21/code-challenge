from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        author_id = cursor.lastrowid
        return cls(name, id=author_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], id=row[0])
        return None

    def articles(self):
        """Returns list of all articles written by the author"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles 
            WHERE author_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def magazines(self):
        """Returns unique list of magazines the author has contributed to"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def add_article(self, magazine_id, title):
        """Creates and inserts a new Article into the database"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?)
        """, (title, self.id, magazine_id))
        conn.commit()
        return cursor.lastrowid

    def topic_areas(self):
        """Returns unique list of categories of magazines the author has contributed to"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        return [row[0] for row in cursor.fetchall()]

    @classmethod
    def most_prolific(cls):
        """Find the author who has written the most articles"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, COUNT(art.id) as article_count 
            FROM authors a
            LEFT JOIN articles art ON a.id = art.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return cls(row[1], id=row[0])
        return None
