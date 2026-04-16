from .db import get_db_connection

class Ingredient:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def get_or_create(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM ingredients WHERE name = ?", (name,)).fetchone()
        
        if row:
            conn.close()
            return cls(**dict(row))
            
        cursor.execute("INSERT INTO ingredients (name) VALUES (?)", (name,))
        conn.commit()
        ingredient_id = cursor.lastrowid
        conn.close()
        
        return cls(id=ingredient_id, name=name)

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM ingredients ORDER BY name ASC").fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]
