# seed.py: Populate the database with initial data

from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Insert Authors
    authors = ["Alice Smith", "Bob Johnson", "Charlie Rose"]
    for name in authors:
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))

    # Insert Magazines
    magazines = [
        ("Tech Weekly", "Technology"),
        ("Health Monthly", "Health"),
        ("Art & Culture", "Art")
    ]
    for name, category in magazines:
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))

    # Insert Articles
    articles = [
        ("AI in 2025", 1, 1),
        ("Meditation Benefits", 2, 2),
        ("Modern Art Trends", 3, 3),
        ("Tech for Good", 1, 1),
        ("Healthy Eating", 2, 2),
        ("Gallery Reviews", 3, 3),
        ("Cultural Commentary", 1, 3)
    ]
    for title, author_id, magazine_id in articles:
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (title, author_id, magazine_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully.")
