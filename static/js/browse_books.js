// Autocomplete suggestions
document.getElementById('searchQuery').addEventListener('input', function() {
    const query = this.value.toLowerCase();
    const books = document.querySelectorAll('.book');
    
    books.forEach(book => {
        const title = book.getAttribute('data-title');
        if (title.includes(query)) {
            book.style.display = 'block';
        } else {
            book.style.display = 'none';
        }
    });
});