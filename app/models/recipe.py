from .db import get_db_connection

class Recipe:
    def __init__(self, id, user_id, title, description, steps, is_public, created_at):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.steps = steps
        self.is_public = is_public
        self.created_at = created_at

    @classmethod
    def create(cls, user_id, title, description, steps, is_public=1, ingredients_data=None):
        """
        ingredients_data 格式: [(ingredient_id, quantity), ...]
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO recipes (user_id, title, description, steps, is_public) VALUES (?, ?, ?, ?, ?)",
                (user_id, title, description, steps, is_public)
            )
            recipe_id = cursor.lastrowid

            if ingredients_data:
                for ing_id, quantity in ingredients_data:
                    cursor.execute(
                        "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)",
                        (recipe_id, ing_id, quantity)
                    )
            conn.commit()
            return recipe_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
        conn.close()
        if row:
            return cls(**dict(row))
        return None

    @classmethod
    def get_all(cls, public_only=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM recipes "
        if public_only:
            query += "WHERE is_public = 1 "
        query += "ORDER BY created_at DESC"
        
        rows = cursor.execute(query).fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def update(cls, recipe_id, title, description, steps, is_public):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE recipes SET title = ?, description = ?, steps = ?, is_public = ? WHERE id = ?",
            (title, description, steps, is_public, recipe_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()

    @classmethod
    def search_by_ingredients(cls, ingredient_ids):
        """
        輸入食材 ID 陣列，包含所選*所有*食材的食譜才會回傳 (AND 邏輯)
        """
        if not ingredient_ids:
            return []
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?'] * len(ingredient_ids))
        query = f"""
            SELECT r.*
            FROM recipes r
            JOIN recipe_ingredients ri ON r.id = ri.recipe_id
            WHERE ri.ingredient_id IN ({placeholders}) AND r.is_public = 1
            GROUP BY r.id
            HAVING COUNT(DISTINCT ri.ingredient_id) = ?
            ORDER BY r.created_at DESC
        """
        
        params = ingredient_ids + [len(ingredient_ids)]
        rows = cursor.execute(query, params).fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]
