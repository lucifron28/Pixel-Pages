from flask import Blueprint, jsonify, session, current_app
from flask_login import login_required, current_user
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import reader
from models import Book, UserBook, db
import os
import traceback

chapters_bp = Blueprint('chapters', __name__)


@chapters_bp.route("/chapter/<int:chapter_id>")
@login_required
def chapter(chapter_id):
    try:
        # Get the file from session
        file = session.get("file")
        if not file:
            return jsonify({"error": "No book selected"}), 400

        # Load images and check if successful
        if not reader.load_images(file):
            return jsonify({"error": "Failed to load book images"}), 500

        # Load the eBook and get the list of chapters
        book_path = os.path.join(current_app.config['BASE_DIR'], 'ebooks', file)
        if not os.path.exists(book_path):
            return jsonify({"error": "Book file not found"}), 404

        book = epub.read_epub(book_path)
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
            img['src'] = f"/ebook_images/{img_src}"

        # Save the last read chapter in the database
        book = Book.query.filter_by(file=file).first()
        if book:
            user_book = UserBook.query.filter_by(user_id=current_user.id, book_id=book.id).first()
            if user_book:
                user_book.last_read_chapter = chapter_id
                db.session.commit()

        # Return the chapter content as JSON
        return jsonify({"content": str(soup)})

    except Exception as e:
        # Log the full error for debugging
        print(f"Error in chapter route: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500