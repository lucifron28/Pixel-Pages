// Function to hide flash messages after a certain time
function hideFlashes() {
	const flashes = document.querySelectorAll('.flash');
	flashes.forEach(flash => {
		setTimeout(() => {
			flash.style.display = 'none';
		}, 3000); // 3000 milliseconds = 3 seconds
	});
}

// Call the function to hide flash messages
document.addEventListener('DOMContentLoaded', hideFlashes);

// Autocomplete suggestions
document.getElementById('searchQuery').addEventListener('input', function() {
	const query = this.value;
	if (query.length > 2) {
		fetch(`/autocomplete?query=${query}`)
			.then(response => response.json())
			.then(data => {
				const suggestions = data.suggestions;
				const suggestionsContainer = document.getElementById('autocomplete-suggestions');
				suggestionsContainer.innerHTML = '';
				suggestions.forEach(suggestion => {
					const suggestionElement = document.createElement('div');
					suggestionElement.textContent = suggestion;
					suggestionElement.addEventListener('click', () => {
						document.getElementById('searchQuery').value = suggestion;
						suggestionsContainer.innerHTML = '';
					});
					suggestionsContainer.appendChild(suggestionElement);
				});
			});
	}
});

// Search form submission
document.getElementById('searchForm').addEventListener('submit', function(event) {
	event.preventDefault();
	document.getElementById('loading-spinner').style.display = 'block';
	const query = document.getElementById('searchQuery').value;
	fetch(`/search?query=${query}`)
		.then(response => response.json())
		.then(data => {
			document.getElementById('loading-spinner').style.display = 'none';
			const book = data.book;
			document.getElementById('description').textContent = book.description;
			document.getElementById('category').textContent = book.category;
			document.getElementById('thumbnail').src = book.thumbnail;
			document.getElementById('thumbnail').style.display = 'block';
		});
});

// Book details modal
document.getElementById('result').addEventListener('click', function(event) {
	if (event.target.tagName === 'P' || event.target.tagName === 'IMG') {
		const description = document.getElementById('description').textContent;
		const category = document.getElementById('category').textContent;
		const thumbnail = document.getElementById('thumbnail').src;
		document.getElementById('modal-title').textContent = description;
		document.getElementById('modal-description').textContent = description;
		document.getElementById('modal-category').textContent = category;
		document.getElementById('modal-thumbnail').src = thumbnail;
		document.getElementById('bookModal').style.display = 'block';
	}
});

document.querySelector('.close').addEventListener('click', function() {
	document.getElementById('bookModal').style.display = 'none';
});