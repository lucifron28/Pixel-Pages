from flask import Flask, render_template, session
from flask_login import LoginManager, login_required
from dotenv import load_dotenv
from models import db, User
from blueprints.auth import auth_bp
from blueprints.books import books_bp
from blueprints.chapters import chapters_bp
from blueprints.search import search_bp
import os
import reader
from config import Config
import ebooklib
from ebooklib import epub
from api_service import fetch_book_details

# Ensure images are loaded from the correct EPUB file
reader.load_images()
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
app.register_blueprint(books_bp, url_prefix='/books')
app.register_blueprint(chapters_bp)
app.register_blueprint(search_bp, url_prefix='/search')

@app.route("/")
@login_required
def index():
    # Load the eBook and get the list of chapters
    book = epub.read_epub(f"static/ebooks/{reader.book_file}")
    chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    
    # Retrieve the last read chapter from the session, default to 0 if not set
    last_read_chapter = session.get('last_read_chapter', 0)
    print(f"Last read chapter retrieved from session: {last_read_chapter}")
    
    # Render the index page with the number of chapters and the last read chapter
    return render_template("index.html", chapters=len(chapters), last_read_chapter=last_read_chapter)


# Create the database if it doesn't exist
if not os.path.exists('users.db'):
    with app.app_context():
        db.create_all()
        print("Database created!")

if __name__ == "__main__":
    app.run(debug=True)