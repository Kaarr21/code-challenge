from lib.db.connection import get_connection

class Author:
    def __init__(self, id, name):
        """
        Initialize an Author instance.
        
        Args:
            id (int): The author's unique identifier
            name (str): The author's name
            
        The validation ensures name is a string with at least 1 character.
        """
        self.id = id
        self._name = None
        self.name = name  # Use property setter for validation
    
    @property
    def name(self):
        """Get the author's name."""
        return self._name
    
    @name.setter
    def name(self, value):
        """
        Set the author's name with validation.
        
        Args:
            value (str): The name to set
            
        Raises:
            ValueError: If name is not a string or is empty
        """
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()
    
    def save(self):
        """
        Save this author to the database.
        Updates existing record if id exists, otherwise creates new record.
        
        Returns:
            bool: True if save was successful
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id:
                # Update existing author
                cursor.execute(
                    "UPDATE authors SET name = ? WHERE id = ?",
                    (self.name, self.id)
                )
            else:
                # Create new author
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self.id = cursor.lastrowid
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error saving author: {e}")
            return False
        finally:
            conn.close()
    
    @classmethod
    def all(cls):
        """
        Retrieve all authors from the database.
        
        Returns:
            list[Author]: List of all Author instances
            
        This is a class method because it operates on the class itself,
        not on a specific instance. It returns multiple Author objects.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], name=row['name']) for row in rows]
    
    @classmethod
    def find_by_id(cls, author_id):
        """
        Find an author by their ID.
        
        Args:
            author_id (int): The ID to search for
            
        Returns:
            Author or None: Author instance if found, None otherwise
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row['id'], name=row['name']) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """
        Find an author by their name.
        
        Args:
            name (str): The name to search for
            
        Returns:
            Author or None: First author with matching name, None if not found
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row['id'], name=row['name']) if row else None
    
    def articles(self):
        """
        Get all articles written by this author.
        
        Returns:
            list[Article]: List of Article instances written by this author
            
        Uses a lazy import to avoid circular imports between Author and Article.
        """
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row['id'], title=row['title'], content=row['content'], 
                       author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]
    
    def magazines(self):
        """
        Get all unique magazines this author has contributed to.
        
        Returns:
            list[Magazine]: List of unique Magazine instances
            
        Uses a JOIN query to find magazines through the articles relationship.
        DISTINCT ensures each magazine appears only once.
        """
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
        return [Magazine(id=row['id'], name=row['name'], category=row['category']) for row in rows]
    
    def add_article(self, magazine, title, content=""):
        """
        Create a new article by this author for the given magazine.
        
        Args:
            magazine (Magazine): The magazine to publish in
            title (str): The article title
            content (str): The article content (optional)
            
        Returns:
            Article or None: The created Article instance, or None if creation failed
            
        This method creates a new article and saves it to the database.
        """
        from lib.models.article import Article
        
        if not title or not isinstance(title, str):
            print("Title must be a non-empty string")
            return None
            
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            """, (title.strip(), content, self.id, magazine.id))
            
            article_id = cursor.lastrowid
            conn.commit()
            
            return Article(id=article_id, title=title.strip(), content=content,
                         author_id=self.id, magazine_id=magazine.id)
        except Exception as e:
            conn.rollback()
            print(f"Error creating article: {e}")
            return None
        finally:
            conn.close()
    
    def topic_areas(self):
        """
        Get unique categories of magazines this author has contributed to.
        
        Returns:
            list[str]: List of unique magazine categories
            
        This uses DISTINCT to ensure each category appears only once,
        even if the author has written multiple articles in that category.
        """
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
        return [row['category'] for row in rows]
    
    def __repr__(self):
        """String representation of the Author for debugging."""
        return f"<Author {self.id}: {self.name}>"
        
