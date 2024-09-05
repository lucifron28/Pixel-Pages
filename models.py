from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID of the user
    username = db.Column(db.String(150), unique=True, nullable=False) # Username of the user
    password = db.Column(db.String(150), nullable=False) # Password of the user
    books = db.relationship('Book', backref='owner', lazy=True)  # Relationship to Book

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID of the book
    title = db.Column(db.String(150), nullable=False) # Title of the book
    author = db.Column(db.String(150), nullable=False) # Author of the book
    file = db.Column(db.String(150), nullable=False) # File path
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    thumbnail = db.Column(db.String(150), nullable=False)
    user_books = db.relationship('User', backref='book', lazy=True)  # Relationship to User


class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID of the user book
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key to User
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False) # Foreign key to Book
    last_read_chapter = db.Column(db.Integer, nullable=False) # Last read chapter