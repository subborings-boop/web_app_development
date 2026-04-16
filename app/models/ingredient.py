from .db import get_db_connection

class Ingredient:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, data):
        """
        新增一筆 Ingredient 記錄。
        參數 data 需包含 {'name': '食材名稱'}
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ingredients (name) VALUES (?)", (data.get('name'),))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def get_or_create(cls, name):
        """依照名稱取得單筆 Ingredient，若不存在則建立"""
        conn = get_db_connection()
        try:
            row = conn.execute("SELECT * FROM ingredients WHERE name = ?", (name,)).fetchone()
            if row:
                return cls(**dict(row))
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ingredients (name) VALUES (?)", (name,))
            conn.commit()
            return cls(id=cursor.lastrowid, name=name)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, ingredient_id):
        """取得單筆記錄"""
        conn = get_db_connection()
        try:
            row = conn.execute("SELECT * FROM ingredients WHERE id = ?", (ingredient_id,)).fetchone()
            if row:
                return cls(**dict(row))
            return None
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        """取得所有的 Ingredient 記錄"""
        conn = get_db_connection()
        try:
            rows = conn.execute("SELECT * FROM ingredients ORDER BY name ASC").fetchall()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def update(cls, ingredient_id, data):
        """更新記錄"""
        conn = get_db_connection()
        try:
            fields = []
            values = []
            for k, v in data.items():
                fields.append(f"{k} = ?")
                values.append(v)
            values.append(ingredient_id)
            query = f"UPDATE ingredients SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, tuple(values))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def delete(cls, ingredient_id):
        """刪除記錄"""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM ingredients WHERE id = ?", (ingredient_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
