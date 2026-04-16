from .db import get_db_connection

class User:
    def __init__(self, id, username, email, password_hash, is_admin, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.created_at = created_at

    @classmethod
    def create(cls, data):
        """
        新增一筆 User 記錄。
        參數 data 需包含字典 {'username': '...', 'email': '...', 'password_hash': '...', 'is_admin': 0}
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)",
                (data.get('username'), data.get('email'), data.get('password_hash'), data.get('is_admin', 0))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, user_id):
        """根據 id 取得單筆 User 記錄"""
        conn = get_db_connection()
        try:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row:
                return cls(**dict(row))
            return None
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def get_by_email(cls, email):
        """根據 email 取得單筆 User 記錄"""
        conn = get_db_connection()
        try:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if row:
                return cls(**dict(row))
            return None
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        """取得所有的 User 記錄"""
        conn = get_db_connection()
        try:
            rows = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def update(cls, user_id, data):
        """
        更新記錄。data 需為 dict。
        """
        conn = get_db_connection()
        try:
            fields = []
            values = []
            for k, v in data.items():
                fields.append(f"{k} = ?")
                values.append(v)
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, tuple(values))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def delete(cls, user_id):
        """根據 id 刪除記錄"""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
