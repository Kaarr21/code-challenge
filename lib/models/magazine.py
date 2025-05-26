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
        """
        Creates a new magazine in the database.
        
        How it works:
        1. Validates that name and category are provided
        2. Uses parameterized query to prevent SQL injection
        3. Gets auto-generated ID and returns new Magazine instance
        """
        if not name or not category:
            raise ValueError("Magazine must have a name and category")

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        """
        cursor.execute(sql, (name, category))
        conn.commit()

        magazine_id = cursor.lastrowid
        conn.close()
        return cls(name, category, magazine_id)

    @classmethod
    def find_by_id(cls, id):
        """
        Finds a magazine by ID.
        """
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM magazines WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    @classmethod
    def find_by_name(cls, name):
        """
        Finds a magazine by name.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    @classmethod
    def find_by_category(cls, category):
        """
        Finds all magazines in a specific category.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], category=row[2]) for row in rows]

    def articles(self):
        """
        Returns all articles published in this magazine.
        
        How it works:
        1. JOINs articles with authors to get complete information
        2. Filters by this magazine's ID
        3. Returns list of dictionaries with article and author info
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, au.name as author_name
            FROM articles a
            JOIN authors au ON a.author_id = au.id
            WHERE a.magazine_id = ?
        """, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [dict(article) for article in articles]

    def contributors(self):
        """
        Returns unique list of authors who have written for this magazine.
        
        How it works:
        1. Uses DISTINCT to eliminate duplicate authors
        2. JOINs authors table through articles table
        3. Filters by this magazine's ID
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT au.*
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [dict(author) for author in authors]

    def article_titles(self):
        """
        Returns list of titles of all articles in this magazine.
        
        How it works:
        1. Simple SELECT for just titles
        2. Filters by this magazine's ID
        3. Returns list of title strings
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [row['title'] for row in titles]

    def contributing_authors(self):
        """
        Returns authors who have written more than 2 articles for this magazine.
        
        How it works:
        1. Groups articles by author using GROUP BY
        2. Uses HAVING clause to filter groups (authors) with COUNT > 2
        3. HAVING is like WHERE but for grouped results
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT au.*, COUNT(a.id) as article_count
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
            GROUP BY au.id, au.name
            HAVING COUNT(a.id) > 2
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [dict(author) for author in authors]

    @classmethod
    def top_publisher(cls):
        """
        BONUS: Returns the magazine with the most articles.
        
        How it works:
        1. JOINs magazines with articles
        2. Groups by magazine to count articles per magazine
        3. Orders by count in descending order
        4. LIMIT 1 gets just the top result
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id, m.name, m.category
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    def update(self, name=None, category=None):
        """
        Updates magazine information.
        
        How it works:
        1. Updates instance attributes if new values provided
        2. Executes UPDATE SQL statement
        3. Uses WHERE clause to update only this specific magazine
        """
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
        conn.close()

    def delete(self):
        """
        Deletes this magazine from the database.
        Note: This will fail if there are articles referencing this magazine
        due to foreign key constraints.
        """
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM magazines WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        conn.close()
        