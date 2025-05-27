from lib.db.connection import get_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        """
        Initialize an Article instance.
        
        Args:
            id (int): The article's unique identifier
            title (str): The article's title
            content (str): The article's content
            author_id (int): ID of the author who wrote this article
            magazine_id (int): ID of the magazine that published this article
        """
        self.id = id
        self._title = None
        self.title = title  # Use property setter for validation
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
    
    @property
    def title(self):
        """Get the article's title."""
        return self._title
    
    @title.setter
    def title(self, value):
        """
        Set the article's title with validation.
        
        Args:
            value (str): The title to set
            
        Raises:
            ValueError: If title is not a string or is empty
        """
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Title must be a non-empty string")
        self._title = value.strip()
    
    def save(self):
        """
        Save this article to the database.
        Updates existing record if id exists, otherwise creates new record.
        
        Returns:
            bool: True if save was successful
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id:
                # Update existing article
                cursor.execute("""
                    UPDATE articles 
                    SET title = ?, content = ?, author_id = ?, magazine_id = ? 
                    WHERE id = ?
                """, (self.title, self.content, self.author_id, self.magazine_id, self.id))
            else:
                # Create new article
                cursor.execute("""
                    INSERT INTO articles (title, content, author_id, magazine_id) 
                    VALUES (?, ?, ?, ?)
                """, (self.title, self.content, self.author_id, self.magazine_id))
                self.id = cursor.lastrowid
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error saving article: {e}")
            return False
        finally:
            conn.close()
    
    @classmethod
    def all(cls):
        """
        Retrieve all articles from the database.
        
        Returns:
            list[Article]: List of all Article instances
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], content=row['content'],
                   author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]
    
    @classmethod
    def find_by_id(cls, article_id):
        """
        Find an article by its ID.
        
        Args:
            article_id (int): The ID to search for
            
        Returns:
            Article or None: Article instance if found, None otherwise
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row['id'], title=row['title'], content=row['content'],
                  author_id=row['author_id'], magazine_id=row['magazine_id']) if row else None
    
    @classmethod
    def find_by_title(cls, title):
        """
        Find articles by title (partial match).
        
        Args:
            title (str): The title to search for
            
        Returns:
            list[Article]: List of articles with matching titles
            
        Uses LIKE operator for partial string matching.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title LIKE ?", (f"%{title}%",))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], content=row['content'],
                   author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]
    
    @classmethod
    def find_by_author(cls, author_id):
        """
        Find all articles written by a specific author.
        
        Args:
            author_id (int): The author's ID
            
        Returns:
            list[Article]: List of articles by the specified author
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], content=row['content'],
                   author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]
    
    @classmethod
    def find_by_magazine(cls, magazine_id):
        """
        Find all articles published in a specific magazine.
        
        Args:
            magazine_id (int): The magazine's ID
            
        Returns:
            list[Article]: List of articles in the specified magazine
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], content=row['content'],
                   author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]
    
    def author(self):
        """
        Get the Author instance who wrote this article.
        
        Returns:
            Author or None: Author instance if found, None otherwise
            
        Uses lazy import to avoid circular import issues.
        """
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        conn.close()
        return Author(id=row['id'], name=row['name']) if row else None
    
    def magazine(self):
        """
        Get the Magazine instance that published this article.
        
        Returns:
            Magazine or None: Magazine instance if found, None otherwise
            
        Uses lazy import to avoid circular import issues.
        """
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return Magazine(id=row['id'], name=row['name'], category=row['category']) if row else None
    
    def __repr__(self):
        """String representation of the Article for debugging."""
        return f"<Article {self.id}: '{self.title}' by Author {self.author_id} in Magazine {self.magazine_id}>"
        