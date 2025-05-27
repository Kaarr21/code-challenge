import sqlite3
from lib.db.connection import get_connection

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction.
    
    Args:
        author_name (str): Name of the author to create
        articles_data (list): List of dicts with 'title', 'content', and 'magazine_id' keys
        
    Returns:
        tuple: (success: bool, author_id: int or None, error_message: str or None)
        
    Example:
        articles = [
            {"title": "AI in Healthcare", "content": "Content here...", "magazine_id": 1},
            {"title": "Future of Medicine", "content": "More content...", "magazine_id": 2}
        ]
        success, author_id, error = add_author_with_articles("Dr. Smith", articles)
    """
    if not author_name or not isinstance(author_name, str):
        return False, None, "Author name must be a non-empty string"
    
    if not articles_data or not isinstance(articles_data, list):
        return False, None, "Articles data must be a non-empty list"
    
    # Validate article data structure
    for i, article in enumerate(articles_data):
        if not isinstance(article, dict):
            return False, None, f"Article {i} must be a dictionary"
        
        required_fields = ['title', 'magazine_id']
        for field in required_fields:
            if field not in article:
                return False, None, f"Article {i} missing required field: {field}"
        
        if not article['title'] or not isinstance(article['title'], str):
            return False, None, f"Article {i} title must be a non-empty string"
    
    conn = get_connection()
    
    try:
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Insert author
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (author_name.strip(),)
        )
        author_id = cursor.lastrowid
        
        # Insert articles
        for i, article in enumerate(articles_data):
            title = article['title'].strip()
            content = article.get('content', '').strip()  # Default to empty string if not provided
            magazine_id = article['magazine_id']
            
            # Verify magazine exists before inserting article
            cursor.execute("SELECT id FROM magazines WHERE id = ?", (magazine_id,))
            if not cursor.fetchone():
                raise ValueError(f"Magazine with ID {magazine_id} does not exist (article {i})")
            
            cursor.execute(
                "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                (title, content, author_id, magazine_id)
            )
        
        # Commit transaction
        conn.commit()
        print(f"Transaction successful: Created author '{author_name}' with {len(articles_data)} articles")
        return True, author_id, None
        
    except Exception as e:
        # Rollback on any error
        conn.rollback()
        error_msg = f"Transaction failed: {str(e)}"
        print(error_msg)
        return False, None, error_msg
        
    finally:
        conn.close()

def delete_author_and_articles(author_id):
    """
    Delete an author and all their articles in a single transaction.
    
    Args:
        author_id (int): ID of the author to delete
        
    Returns:
        tuple: (success: bool, deleted_articles_count: int, error_message: str or None)
    """
    if not isinstance(author_id, int) or author_id <= 0:
        return False, 0, "Author ID must be a positive integer"
    
    conn = get_connection()
    
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Check if author exists
        cursor.execute("SELECT name FROM authors WHERE id = ?", (author_id,))
        author_row = cursor.fetchone()
        if not author_row:
            raise ValueError(f"Author with ID {author_id} does not exist")
        
        author_name = author_row['name']
        
        # Count articles to be deleted
        cursor.execute("SELECT COUNT(*) as count FROM articles WHERE author_id = ?", (author_id,))
        article_count = cursor.fetchone()['count']
        
        # Delete articles first (due to foreign key constraint)
        cursor.execute("DELETE FROM articles WHERE author_id = ?", (author_id,))
        
        # Delete author
        cursor.execute("DELETE FROM authors WHERE id = ?", (author_id,))
        
        conn.commit()
        print(f"Successfully deleted author '{author_name}' and {article_count} articles")
        return True, article_count, None
        
    except Exception as e:
        conn.rollback()
        error_msg = f"Deletion failed: {str(e)}"
        print(error_msg)
        return False, 0, error_msg
        
    finally:
        conn.close()

def transfer_articles_between_magazines(from_magazine_id, to_magazine_id):
    """
    Transfer all articles from one magazine to another in a single transaction.
    
    Args:
        from_magazine_id (int): Source magazine ID
        to_magazine_id (int): Target magazine ID
        
    Returns:
        tuple: (success: bool, transferred_count: int, error_message: str or None)
    """
    if not all(isinstance(mid, int) and mid > 0 for mid in [from_magazine_id, to_magazine_id]):
        return False, 0, "Magazine IDs must be positive integers"
    
    if from_magazine_id == to_magazine_id:
        return False, 0, "Source and target magazines cannot be the same"
    
    conn = get_connection()
    
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Verify both magazines exist
        cursor.execute("SELECT name FROM magazines WHERE id IN (?, ?)", 
                      (from_magazine_id, to_magazine_id))
        magazines = cursor.fetchall()
        
        if len(magazines) != 2:
            missing_ids = []
            existing_ids = [mag['id'] for mag in magazines] if magazines else []
            for mid in [from_magazine_id, to_magazine_id]:
                if mid not in existing_ids:
                    missing_ids.append(mid)
            raise ValueError(f"Magazine(s) with ID(s) {missing_ids} do not exist")
        
        # Count articles to be transferred
        cursor.execute("SELECT COUNT(*) as count FROM articles WHERE magazine_id = ?", 
                      (from_magazine_id,))
        transfer_count = cursor.fetchone()['count']
        
        if transfer_count == 0:
            return True, 0, "No articles to transfer"
        
        # Transfer articles
        cursor.execute(
            "UPDATE articles SET magazine_id = ? WHERE magazine_id = ?",
            (to_magazine_id, from_magazine_id)
        )
        
        conn.commit()
        print(f"Successfully transferred {transfer_count} articles between magazines")
        return True, transfer_count, None
        
    except Exception as e:
        conn.rollback()
        error_msg = f"Transfer failed: {str(e)}"
        print(error_msg)
        return False, 0, error_msg
        
    finally:
        conn.close()
        