function loadChapter(id) {
    // Show loading state
    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = '<div class="loading">Loading chapter...</div>';

    // Disable navigation buttons while loading
    document.getElementById('prev-chapter').disabled = true;
    document.getElementById('next-chapter').disabled = true;

    fetch(`/chapter/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                contentDiv.innerHTML = `<div class="error-message">${data.error}</div>`;
            } else {
                contentDiv.innerHTML = data.content;
            }
        })
        .catch(error => {
            console.error('Error loading chapter:', error);
            contentDiv.innerHTML = `<div class="error-message">Failed to load chapter. Please try again.</div>`;
        })
        .finally(() => {
            // Re-enable navigation buttons
            document.getElementById('prev-chapter').disabled = false;
            document.getElementById('next-chapter').disabled = false;
        });
}

// Load the last read chapter on page load
document.addEventListener('DOMContentLoaded', () => {
    // Add loading indicator styles
    const style = document.createElement('style');
    style.textContent = `
        .loading {
            text-align: center;
            padding: 20px;
            font-style: italic;
            color: #666;
        }
        .error-message {
            color: #dc3545;
            padding: 20px;
            text-align: center;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            margin: 10px 0;
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
    `;
    document.head.appendChild(style);

    // Load initial chapter
    loadChapter(currentChapter);
});

document.getElementById('prev-chapter').addEventListener('click', () => {
    if (currentChapter > 0) {
        currentChapter--;
        loadChapter(currentChapter);
    }
});

document.getElementById('next-chapter').addEventListener('click', () => {
    if (currentChapter < totalChapters - 1) {
        currentChapter++;
        loadChapter(currentChapter);
    }
});



// script for api fetched from google books api via python requests
