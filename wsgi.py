# app/wsgi.py

# imports
from app import create_app

# Create the application instance
app = create_app()

# The rest handled by WSGI server