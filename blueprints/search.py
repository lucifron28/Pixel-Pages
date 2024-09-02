from flask import Blueprint, jsonify, request
from flask_login import login_required
from api_service import fetch_book_details

search_bp = Blueprint('search', __name__)

@search_bp.route("/search")
@login_required
def search():
    query = request.args.get('query')
    if query:
        book_details = fetch_book_details(query)
        return jsonify(book=book_details)
    return jsonify(error="No query provided"), 400

@search_bp.route("/autocomplete")
@login_required
def autocomplete():
    query = request.args.get('query')
    if query:
        book_details = fetch_book_details(query)
        suggestions = [book_details['title']] if 'title' in book_details else []
        return jsonify(suggestions=suggestions)
    return jsonify(suggestions=[])