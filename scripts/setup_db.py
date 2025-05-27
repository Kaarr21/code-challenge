# setup_db.py: Initializes and seeds the database

import sqlite3
import os

SCHEMA_PATH = "lib/db/schema.sql"
DB_PATH = "articles.db"

# Step 1: Create schema
def setup_schema():
    if not os.path.exists(SCHEMA_PATH):
        print("Schema file not found.")
        return

    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Schema created.")

# Step 2: Seed data
def seed_database():
    from lib.db.seed import seed_data
    seed_data()

if __name__ == "__main__":
    setup_schema()
    seed_database()
    print("Database setup complete.")
