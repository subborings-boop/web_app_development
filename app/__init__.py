import os
import sqlite3
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊所有在 routes 定義的 Blueprints
    from .routes import auth_bp, recipe_bp, main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)

    return app

def init_db(app):
    with app.app_context():
        db_path = app.config['DATABASE']
        db = sqlite3.connect(db_path)
        schema_path = os.path.join(os.path.dirname(app.root_path), 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()
