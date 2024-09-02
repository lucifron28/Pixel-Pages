from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from models import db, Book
import os

books_bp = Blueprint('books', __name__)

@books_bp.route("/browse_books")
@login_required
def browse_books():
    return render_template("browse_books.html")

@books_bp.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['file']
        
        # Save the uploaded file
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        
        # Process the uploaded file (e.g., extract metadata, save to database)
        book = Book(title=title, author=author, file=file.filename, user_id=current_user.id)
        db.session.add(book)
        db.session.commit()
        
        flash('Ebook uploaded successfully.', 'success')
        return redirect(url_for('books.browse_books'))
    
    return render_template("upload.html")