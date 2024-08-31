from flask import Flask, render_template, jsonify, session, redirect, request, flash, url_for
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from api_service import fetch_book_details
import os
import reader
from dotenv import load_dotenv
from models import db, User, Book
from blueprints.auth import auth_bp

# Ensure images are loaded from the correct EPUB file
reader.load_images()
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/ebooks'

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

@app.route("/chapter/<int:chapter_id>")
@login_required
def chapter(chapter_id):
    # Load the eBook and get the list of chapters
    book = epub.read_epub(f"static/ebooks/{reader.book_file}")
    chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    
    # Check if the chapter id is valid
    if chapter_id < 0 or chapter_id >= len(chapters):
        return jsonify({"error": "Chapter not found"}), 404

    # Get the content of the chapter
    chapter_content = chapters[chapter_id].get_body_content().decode('utf-8')

    # Parse the chapter content and update image src paths
    soup = BeautifulSoup(chapter_content, 'html.parser')
    for img in soup.find_all('img'):
        img_src = img['src'].split('/')[-1]  # Get the image filename
        img['src'] = f"/static/ebook_images/{img_src}"

    # Save the last read chapter in the session
    session['last_read_chapter'] = chapter_id
    print(f"Saved last read chapter in session: {session['last_read_chapter']}")  # Debugging print
    # Return the chapter content as JSON
    return jsonify({"content": str(soup)})

@app.route("/browse_books")
@login_required
def browse_books():
    return render_template("browse_books.html")

@app.route("/search")
@login_required
def search():
    query = request.args.get('query')
    if query:
        book_details = fetch_book_details(query)
        return jsonify(book=book_details)
    return jsonify(error="No query provided"), 400

@app.route("/autocomplete")
@login_required
def autocomplete():
    query = request.args.get('query')
    if query:
        book_details = fetch_book_details(query)
        suggestions = [book_details['title']] if 'title' in book_details else []
        return jsonify(suggestions=suggestions)
    return jsonify(suggestions=[])

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['file']
        
        # Save the uploaded file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        # Process the uploaded file (e.g., extract metadata, save to database)
        book = Book(title=title, author=author, file=file.filename)
        db.session.add(book)
        db.session.commit()
        
        flash('Ebook uploaded successfully.', 'success')
        return redirect(url_for('index'))
    
    return render_template("upload.html")

# Create the database if it doesn't exist
if not os.path.exists('users.db'):
    with app.app_context():
        db.create_all()
        print("Database created!")

if __name__ == "__main__":
    app.run(debug=True)