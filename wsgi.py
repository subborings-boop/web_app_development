import sys, os
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from app import create_app, init_db

app = create_app()

def setup_database():
    db_path = app.config['DATABASE']
    if not os.path.exists(db_path):
        print(f"Initializing database at {db_path}...")
        init_db(app)
        print("Database initialized successfully.")

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, use_reloader=False)
