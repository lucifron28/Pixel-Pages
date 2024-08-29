import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

def fetch_book_details(query):
    """Fetch book details including title, authors, published date, thumbnail, description, and category from Google Books API."""
    api_url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}'
    print(api_url)
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            book = data['items'][0]  # Get the first book result
            volume_info = book.get('volumeInfo', {})
            title = volume_info.get('title', 'No title available')
            authors = volume_info.get('authors', ['No author available'])
            published_date = volume_info.get('publishedDate', 'No date available')
            thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
            description = volume_info.get('description', 'No description available')
            categories = volume_info.get('categories', ['No category available'])

            return {
                'title': title,
                'authors': authors,
                'published_date': published_date,
                'thumbnail': thumbnail,
                'description': description,
                'category': categories[0] if categories else 'No category available'
            }
        else:
            return {'error': 'No books found.'}
    else:
        return {'error': 'Failed to fetch data from Google Books API.'}

print(fetch_book_details("I hope this doesn't find you"))