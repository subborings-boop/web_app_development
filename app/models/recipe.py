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
    def create(cls, data):
        """
        新增一筆 Recipe 記錄。
        參數 data 需包含字典，其中 ingredients_data 代表多對多關聯陣列。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recipes (user_id, title, description, steps, is_public) VALUES (?, ?, ?, ?, ?)",
                (data.get('user_id'), data.get('title'), data.get('description'), data.get('steps'), data.get('is_public', 1))
            )
            recipe_id = cursor.lastrowid
            
            ingredients_data = data.get('ingredients_data')
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
        """取得單筆記錄"""
        conn = get_db_connection()
        try:
            row = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
            if not row:
                return None
            return cls(**dict(row))
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def get_ingredients(cls, recipe_id):
        """取得特定食譜關聯的食材紀錄"""
        conn = get_db_connection()
        try:
            rows = conn.execute(
                "SELECT i.id, i.name, ri.quantity FROM recipe_ingredients ri JOIN ingredients i ON ri.ingredient_id = i.id WHERE ri.recipe_id = ?",
                (recipe_id,)
            ).fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def get_all(cls, public_only=True):
        """取得所有的記錄。預設只回傳外觀設為公開(is_public=1)的食譜"""
        conn = get_db_connection()
        try:
            query = "SELECT * FROM recipes"
            if public_only:
                query += " WHERE is_public = 1"
            query += " ORDER BY created_at DESC"
            rows = conn.execute(query).fetchall()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def update(cls, recipe_id, data):
        """更新記錄 (可包含食材關聯更新)"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            update_fields = [k for k in data.keys() if k != 'ingredients_data']
            if update_fields:
                fields_str = ", ".join([f"{k} = ?" for k in update_fields])
                values = [data[k] for k in update_fields]
                values.append(recipe_id)
                cursor.execute(f"UPDATE recipes SET {fields_str} WHERE id = ?", tuple(values))

            if 'ingredients_data' in data:
                cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
                for ing_id, quantity in data['ingredients_data']:
                    cursor.execute(
                        "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)",
                        (recipe_id, ing_id, quantity)
                    )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def delete(cls, recipe_id):
        """刪除記錄"""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def search_by_ingredients(cls, ingredient_ids):
        """從多重食材 id 搜尋符合的食譜"""
        if not ingredient_ids:
            return []
        conn = get_db_connection()
        try:
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
            rows = conn.execute(query, params).fetchall()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()
