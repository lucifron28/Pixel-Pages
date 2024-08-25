import os
import ebooklib
from ebooklib import epub

def load_images():
    # Define the directory to save images
    IMAGES_DIR = 'static/ebook_images'

    # Create the directory if it doesn't exist
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Load the EPUB book
    book = epub.read_epub("static/ebooks/Pride_and_Prejudice.epub")

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
