from flask import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def db_connect(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    image_url = db.Column(db.String(200), nullable=False, default="https://images.unsplash.com/photo-1511367461989-f85a21fda167?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1189&q=80")

    def __repr__(self) -> str:
        return f"User('{self.first_name}','{self.last_name}', '{self.image_url}')"
    
    def fullname(self):
        return f'{self.first_name} {self.last_name}'