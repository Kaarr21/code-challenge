# lib/models/magazine.py

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
        return cls(name, category, magazine_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM magazines WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    def update(self, name=None, category=None):
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

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM magazines WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
