import sqlite3
from flask import current_app

def get_db_connection():
    """
    建立並回傳一個對 SQLite 的連線物件。
    並設置 row_factory = sqlite3.Row 讓查詢結果可以依欄位名稱取值。
    """
    try:
        # 當在 Flask app context 中時
        db_path = current_app.config['DATABASE']
    except Exception:
        # 防止於外部執行測試時報錯
        db_path = 'instance/database.db'
        
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
