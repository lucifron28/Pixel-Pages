# Pixel Pages

#### Video Demo: <>

#### Description:

Pixel Pages is an online ebook library application that allows users to read ebooks, navigate through chapters, and manage their own ebook uploads. It aims to provide a seamless reading experience with features like navigation, image handling, and book search.

## Features

* **User Authentication**: Users can register, log in, and log out.
* **Ebook Reader**: Read and navigate through chapters of EPUB files.
* **Dynamic Image Handling**: Automatically extract and display images from EPUB files.
* **Book Search**: Search for books using the Google Books API.
* **Book Upload**: Authenticated users can upload their own EPUB files.

Please note that some of the features mentioned above are still under development and may not be fully functional at this time.

## Technologies Used

* **Front-End**:
  * HTML/CSS: Structure and styling of web pages.
  * JavaScript: Handling dynamic content.
  * Jinja2: Templating engine for rendering dynamic content.

* **Back-End**:
  * Flask: Web framework for building the application.
  * Flask-Login: User session management.
  * SQLAlchemy: ORM for database interactions.
  * EbookLib: Library for working with EPUB files.
  * BeautifulSoup: Library for parsing HTML content.
  * Google Books API: Fetch book details.

## Project Structure

* `blueprints/`: Directory for flask blueprints
* `blueprints/auth.py`: blueprint for authentication scripts
* `blueprints/books.py`: blueprint for book rendering
* `blueprints/chapters.py: blueprint for saving and loading the chapters
* `app.py`: Main Flask application file.
* `models.py`: Defines database models (`User`, `Book`, `UserBook`) using SQLAlchemy.
* `reader.py`: Manages ebook images.
* `api_service.py`: Fetch book details from Google Books API.
* `static/ebooks/`: Directory for storing EPUB files.
* `static/ebook_images/`: Directory for extracted ebook images.
* `static/js/view_ebook.js`: JavaScript file for handling dynamic content.
* `templates/`: Directory for HTML templates.
  * `base.html`: Base template for the application.
  * `index.html`: Home page template.
  * `login.html`: Login page template.
  * `register.html`: Registration page template.
  * `browse_books.html`: Browse books page template.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/pixel-pages.git
   cd pixel-pages

2. **Install Dependencies**
      Ensure you have Python installed. Then, create a virtual environment (recommended) and install packages from requirements.txt.
      # Create a virtual environment
      python -m venv venv

      # Activate the virtual environment (Linux/Mac)
      source venv/bin/activate

      # Activate the virtual environment (Windows)
      venv\Scripts\activate

      # Install dependencies
      pip install -r requirements.txt

**Future Enhancements**
   Support for multiple ebook formats.
   Improved image handling and resizing.
   Additional features like bookmarks and notes.
   Enhanced search functionality with more filters.