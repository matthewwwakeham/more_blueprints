# app/models.py

# imports
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Database Model ~ Single row with our DB
class User(db.Model):
    # Class Variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    user_color = db.Column(db.String(7), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)