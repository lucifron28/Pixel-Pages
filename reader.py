import os
import ebooklib
from ebooklib import epub
from flask import current_app


def load_images(book_file):
    try:
        # Define the directory to save images using absolute path
        IMAGES_DIR = os.path.join(current_app.config['BASE_DIR'], 'ebook_images')
        EBOOKS_DIR = os.path.join(current_app.config['BASE_DIR'], 'ebooks')

        # Create the directory if it doesn't exist
        os.makedirs(IMAGES_DIR, exist_ok=True)

        # Load the EPUB book using absolute path
        book_path = os.path.join(EBOOKS_DIR, book_file)
        if not os.path.exists(book_path):
            raise FileNotFoundError(f"Book file not found: {book_path}")
            
        book = epub.read_epub(book_path)

        # Save images from the book
        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            image_name = os.path.basename(item.get_name())
            image_path = os.path.join(IMAGES_DIR, image_name)

            # Check if the image file already exists
            if not os.path.exists(image_path):
                with open(image_path, 'wb') as img_file:
                    img_file.write(item.get_content())
                print(f"Saved: {image_name}")
            else:
                print(f"Already exists, skipping: {image_name}")

        print("Images have been extracted and saved.")
        return True
    except Exception as e:
        print(f"Error loading images: {str(e)}")
        return False
