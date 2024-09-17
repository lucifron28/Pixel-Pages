from flask import Flask, render_template, session, redirect, url_for
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db, User
from blueprints.auth import auth_bp
from blueprints.books import books_bp
from blueprints.chapters import chapters_bp
import os
from config import Config

# Ensure images are loaded from the correct EPUB file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(books_bp)
app.register_blueprint(chapters_bp)


@app.route("/")
def index():
    # check if the user is logged in and if not redirect to the login page
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    else:
        # load all user's books
        books = User.query.get(session['user_id']).books

        # load all the book information
        book_info = [{'title': book.title, 'author': book.author, 'thumbnail': book.thumbnail, 'id': book.id} for book in books]

        return render_template("index.html", books=book_info)

# Create the database if it doesn't exist
if not os.path.exists('users.db'):
    with app.app_context():
        db.create_all()
        print("Database created!")

if __name__ == "__main__":
    app.run(debug=True)