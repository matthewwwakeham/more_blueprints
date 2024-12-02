# app/run.py

# imports
from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")
    app.run(debug=True)