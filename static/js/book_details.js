// Autocomplete suggestions
document.getElementById('searchQuery').addEventListener('input', function() {
    const query = this.value.toLowerCase();
    const books = document.querySelectorAll('.browse-books-book');
    
    books.forEach(book => {
        const title = book.getAttribute('data-title');
        if (title.includes(query)) {
            book.style.display = 'Flex';
        } else {
            book.style.display = 'none';
        }
    });
});

// Read more functionality
document.querySelectorAll('.read-more').forEach(link => {
    link.addEventListener('click', function() {
        const description = this.previousElementSibling;
        if (description.style.maxHeight === 'none' || description.style.maxHeight === '') {
            description.style.maxHeight = '100px';
            this.textContent = 'Read more';
        } else {
            description.style.maxHeight = 'none';
            this.textContent = 'Read less';
        }
    });
});