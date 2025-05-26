from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    @classmethod
    def create(cls, name):
        """
        Creates a new author in the database.
        
        How it works:
        1. Gets database connection
        2. Executes INSERT SQL statement with parameterized query (? placeholder)
        3. Commits the transaction to save changes
        4. Gets the auto-generated ID using cursor.lastrowid
        5. Returns new Author instance with the ID
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return cls(name, id=author_id)

    @classmethod
    def find_by_id(cls, id):
        """
        Finds an author by their ID.
        
        How it works:
        1. Executes SELECT query with WHERE clause
        2. fetchone() returns either a Row object or None
        3. If found, creates Author instance using row data
        4. row[0] is ID, row[1] is name (column order from schema)
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], id=row[0])  # name, then id
        return None

    @classmethod
    def find_by_name(cls, name):
        """
        Finds an author by their name.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], id=row[0])
        return None

    def articles(self):
        """
        Returns all articles written by this author.
        
        How it works:
        1. Uses JOIN to combine articles with author and magazine data
        2. WHERE clause filters for this author's ID
        3. Returns list of dictionaries with complete article info
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, au.name as author_name, m.name as magazine_name, m.category
            FROM articles a
            JOIN authors au ON a.author_id = au.id
            JOIN magazines m ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [dict(article) for article in articles]

    def magazines(self):
        """
        Returns unique magazines this author has contributed to.
        
        How it works:
        1. Uses DISTINCT to eliminate duplicate magazines
        2. JOINs magazines table with articles table
        3. Filters by this author's ID
        4. Returns list of magazine dictionaries
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.*
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [dict(magazine) for magazine in magazines]

    def add_article(self, magazine, title):
        """
        Creates a new article for this author in the specified magazine.
        
        Parameters:
        - magazine: Magazine object or magazine_id (integer)
        - title: String title for the article
        
        How it works:
        1. Handles both Magazine object and integer ID input
        2. Creates new article linking this author to the magazine
        3. Returns the created Article object
        """
        from lib.models.article import Article
        
        # Handle both Magazine object and integer ID
        magazine_id = magazine.id if hasattr(magazine, 'id') else magazine
        
        return Article.create(title, self.id, magazine_id)

    def topic_areas(self):
        """
        Returns unique categories of magazines this author has written for.
        
        How it works:
        1. Uses DISTINCT to get unique categories
        2. JOINs magazines through articles table
        3. Returns list of category strings
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        categories = cursor.fetchall()
        conn.close()
        return [row['category'] for row in categories]