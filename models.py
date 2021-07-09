from flask import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    posts = db.relationship('Post', backref='users', cascade='all, delete-orphan')
    def __repr__(self) -> str:
        return f"User('{self.first_name}','{self.last_name}', '{self.image_url}')"
    
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    


class Post(db.Model):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    # user = db.relationship('User',
    #     backref=db.backref('users', lazy=True))
    # tags = db.relationship('Tag', secondary="post_tags", backref='posts',cascade="delete")
class Tag(db.Model):
    __tablename__="tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', backref=db.backref('user'), cascade="all, delete")
class PostTag(db.Model):
    __tablename__="post_tags"
    post_id = db.Column(db.Integer,
                       db.ForeignKey("posts.id"),
                       primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
    