import sqlite3

#the connection to the database.
conn = sqlite3.connect("lib/db/database.db")
cursor = conn.cursor()

#clearing existing data
cursor.execute("DELETE FROM articles")
cursor.execute("DELETE FROM authors")
cursor.execute("DELETE FROM magazines")

#doing an insert into authors
cursor.execute("INSERT INTO authors (name) VALUES ('Fahiye Muhammad')")
cursor.execute("INSERT INTO authors (name) VALUES ('Sadyq Alnuur')")
cursor.execute("INSERT INTO authors (name) VALUES ('Mark Kenyua')")

#Inserting  into magazines 
cursor.execute("INSERT INTO magazines (name, category) VALUES ('Science Monthly', 'Science')")
cursor.execute("INSERT INTO magazines (name, category) VALUES ('Writers Digest', 'Literature')")
cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Africa', 'Technology')")

# Inserting into articles
cursor.execute("""
    INSERT INTO  articles (title, content, author_id, magazine_id)
    VALUES ('The rise of AI in Africa', 'Artificial intelligence is booming across africa...', 1, 3)               
""")
cursor.execute("""
    INSERT INTO articles (title, content, author_id, magazine_id)
    VALUES ('Storytelling as resistance', 'Literature has always been a powerful tool...', 2, 2)
""")
cursor.execute("""
    INSERT INTO articles (title, content, author_id, magazine_id)
    VALUES ('Environmental Challenges', 'Climate chamge continues to affect the continent...', 3, 1)           
""")

conn.commit()
conn.close

print("Database seeded successfully!")


