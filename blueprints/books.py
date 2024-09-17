from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session, jsonify, send_from_directory
from flask_login import login_required, current_user
from models import db, Book, UserBook
import os
from api_service import fetch_book_details
import ebooklib
from ebooklib import epub

books_bp = Blueprint('books', __name__)

@books_bp.route('/ebook_images/<path:filename>')
@login_required
def ebook_images(filename):
    return send_from_directory('ebook_images', filename)

@books_bp.route("/books_details", methods=['GET', 'POST'])
@login_required
def book_details():
    user_books = Book.query.filter_by(user_id=current_user.id).all()
    # fetch all the books of user and display the all the details of the book
    book_details = [fetch_book_details(book.title) for book in user_books]
    return render_template("book_details.html", books=user_books, details=book_details)
    

@books_bp.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['file']
        
        # fetch book details from Google Books API
        book_details = fetch_book_details(title, author)
        thumbnail = book_details.get('thumbnail', 'No thumbnail available')

        # Save the uploaded file
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        
        # Process the uploaded file (e.g., extract metadata, save to database)
        book = Book(title=title, author=author, file=file.filename, user_id=current_user.id, thumbnail=thumbnail)
        db.session.add(book)
        db.session.commit()
        
        flash('Ebook uploaded successfully.', 'success')
        return redirect(url_for('index'))
    
    return render_template("upload.html")

@books_bp.route("/read/<int:book_id>")
@login_required
def read(book_id):
    book = Book.query.get(book_id)
    if book is None:
        flash('Book not found.', 'error')
        return redirect(url_for('index'))

    # Get or create the UserBook entry
    user_book = UserBook.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if user_book is None:
        user_book = UserBook(user_id=current_user.id, book_id=book_id, last_read_chapter=0)
        db.session.add(user_book)
        db.session.commit()

    file = book.file
    session["file"] = file
    book = epub.read_epub(os.path.join(current_app.config['UPLOAD_FOLDER'], file))
    chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    last_read_chapter = user_book.last_read_chapter
    print(f"Last read chapter retrieved from database: {last_read_chapter}")
    return render_template("ebook.html", 
                           chapters=len(chapters), 
                           last_read_chapter=last_read_chapter)


@books_bp.route('/delete/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book and book.user_id == current_user.id:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully.', 'success')
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Book not found or unauthorized'}), 404