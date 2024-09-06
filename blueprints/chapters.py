from flask import Blueprint, jsonify, session
from flask_login import login_required
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import reader

chapters_bp = Blueprint('chapters', __name__)


@chapters_bp.route("/chapter/<int:chapter_id>")
@login_required
def chapter(chapter_id):
    # Load the eBook and get the list of chapters
    file = session.get("file")
    reader.load_images(file)
    book = epub.read_epub(f"static/ebooks/{file}")
    chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    # Check if the chapter id is valid
    # if chapter_id < 0 or chapter_id >= len(chapters):
    #     return jsonify({"error": "Chapter not found"}), 404

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