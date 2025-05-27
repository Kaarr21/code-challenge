from lib.db.connection import get_connection

def seed_database():
    """
    Seeds the database with initial test data.
    This function uses our standardized connection and properly closes resources.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Clear existing data (in reverse order due to foreign key constraints)
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors") 
        cursor.execute("DELETE FROM magazines")
        
        # Insert authors
        cursor.execute("INSERT INTO authors (name) VALUES ('Fahiye Muhammad')")
        cursor.execute("INSERT INTO authors (name) VALUES ('Sadyq Alnuur')")
        cursor.execute("INSERT INTO authors (name) VALUES ('Mark Kenyua')")
        
        # Insert magazines
        cursor.execute("INSERT INTO magazines (name, category) VALUES ('Science Monthly', 'Science')")
        cursor.execute("INSERT INTO magazines (name, category) VALUES ('Writers Digest', 'Literature')")
        cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Africa', 'Technology')")
        
        # Insert articles
        cursor.execute("""
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES ('The rise of AI in Africa', 'Artificial intelligence is booming across africa...', 1, 3)               
        """)
        cursor.execute("""
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES ('Storytelling as resistance', 'Literature has always been a powerful tool...', 2, 2)
        """)
        cursor.execute("""
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES ('Environmental Challenges', 'Climate change continues to affect the continent...', 3, 1)           
        """)
        
        # Add more articles for testing contributing_authors method
        cursor.execute("""
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES ('AI Ethics', 'The ethical implications of AI...', 1, 1)           
        """)
        cursor.execute("""
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES ('Machine Learning Basics', 'Understanding the fundamentals...', 1, 1)           
        """)
        
        conn.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error seeding database: {e}")
    finally:
        conn.close()

# Run seeding if this file is executed directly
if __name__ == "__main__":
    seed_database()

