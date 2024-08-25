# Pixel Pages: Online Ebook Library

## Project Overview

Pixel Pages is an online ebook library application that allows users to read ebooks and navigate through chapters. It aims to provide a seamless reading experience with features like navigation and image handling.

## Current Features

* User Authentication (under development)
* Ebook Reader for reading and navigating chapters
* Dynamic Image Handling for automatically extracting and displaying images

## Technologies Used

* **Flask:** Web framework for building the application.
* **EbookLib:** Library for working with EPUB files.
* **BeautifulSoup:** Library for parsing HTML content.

## Project Structure

* `app.py`: Main Flask application file (routes & logic).
* `reader.py`: Functionality for loading and managing ebook images.
* `static/ebooks/`: Directory for storing EPUB files.
* `static/ebook_images/`: Directory for extracted ebook images.
* `templates/`: Directory for HTML templates.
* `static/script.js`: JavaScript file for handling dynamic content.

## Setup Instructions

1. **Clone the Repository** 
   (Replace with your specific instructions)

2. **Install Dependencies**

   Ensure you have Python installed. Then, create a virtual environment (recommended) and install packages from `requirements.txt`.

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment (Windows/Linux)
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

Future Enhancements:

    User authentication with Flask Login.
    Support for multiple ebook formats.
    Improved image handling and resizing.
    Additional features like bookmarks and notes.
