from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id, name, category):
        """
        Initialize a Magazine instance.
        
        Args:
            id (int): The magazine's unique identifier
            name (str): The magazine's name
            category (str): The magazine's category
            
        Uses properties for validation of name and category.
        """
        self.id = id
        self._name = None
        self._category = None
        self.name = name  # Use property setter for validation
        self.category = category  # Use property setter for validation
    
    @property
    def name(self):
        """Get the magazine's name."""
        return self._name
    
    @name.setter
    def name(self, value):
        """
        Set the magazine's name with validation.
        
        Args:
            value (str): The name to set
            
        Raises:
            ValueError: If name is not a string or is empty
        """
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()
    
    @property
    def category(self):
        """Get the magazine's category."""
        return self._category
    
    @category.setter
    def category(self, value):
        """
        Set the magazine's category with validation.
        
        Args:
            value (str): The category to set
            
        Raises:
            ValueError: If category is not a string or is empty
        """
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value.strip()
    
    def save(self):
        """
        Save this magazine to the database.
        Updates existing record if id exists, otherwise creates new record.
        
        Returns:
            bool: True if save was successful
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id:
                # Update existing magazine
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
            else:
                # Create new magazine
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error saving magazine: {e}")
            return False
        finally:
            conn.close()
    
    @classmethod
    def all(cls):
        """
        Retrieve all magazines from the database.
        
        Returns:
            list[Magazine]: List of all Magazine instances
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], name=row['name'], category=row['category']) for row in rows]
    
    @classmethod
    def find_by_id(cls, magazine_id):
        """
        Find a magazine by its ID.
        
        Args:
            magazine_id (int): The ID to search for
            
        Returns:
            Magazine or None: Magazine instance if found, None otherwise
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row['id'], name=row['name'], category=row['category']) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """
        Find a magazine by its name.
        
        Args:
            name (str): The name to search for
            
        Returns:
            Magazine or None: First magazine with matching name, None if not found
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row['id'], name=row['name'], category=row['category']) if row else None
    
    @classmethod
    def find_by_category(cls, category):
        """
        Find all magazines in a specific category.
        
        Args:
            category (str): The category to search for
            
        Returns:
            list[Magazine]: List of magazines in the specified category
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], name=row['name'], category=row['category']) for row in rows]
    
    def articles(self):
        """
        Get all articles published in this magazine.
        
        Returns:
            list[Article]: List of Article instances published in this magazine
        """
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row['id'], title=row['title'], content=row['content'],
                       author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]
    
    def contributors(self):
        """
        Get all unique authors who have written for this magazine.
        
        Returns:
            list[Author]: List of unique Author instances who have contributed
            
        Uses DISTINCT to ensure each author appears only once,
        even if they've written multiple articles for this magazine.
        """
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
        return [Author(id=row['id'], name=row['name']) for row in rows]
    
    def article_titles(self):
        """
        Get a list of all article titles published in this magazine.
        
        Returns:
            list[str]: List of article titles
            
        This method returns just the titles as strings, not full Article objects.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['title'] for row in rows]
    
    def contributing_authors(self):
        """
        Get authors who have written more than 2 articles for this magazine.
        
        Returns:
            list[Author]: List of Author instances with 2+ articles in this magazine
            
        Uses GROUP BY and HAVING to filter authors by article count.
        The HAVING clause filters groups (authors) based on aggregate functions (COUNT).
        """
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id, authors.name
            HAVING COUNT(articles.id) > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(id=row['id'], name=row['name']) for row in rows]
    
    @classmethod
    def top_publisher(cls):
        """
        Find the magazine with the most articles published.
        
        Returns:
            Magazine or None: Magazine with most articles, None if no magazines exist
            
        This is a class method because it operates on all magazines,
        not a specific instance. Uses ORDER BY and LIMIT to get the top result.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.*, COUNT(articles.id) as article_count
            FROM magazines
            LEFT JOIN articles ON articles.magazine_id = magazines.id
            GROUP BY magazines.id, magazines.name, magazines.category
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        return cls(id=row['id'], name=row['name'], category=row['category']) if row else None
    
    def __repr__(self):
        """String representation of the Magazine for debugging."""
        return f"<Magazine {self.id}: {self.name} ({self.category})>"
