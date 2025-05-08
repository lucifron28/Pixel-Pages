document.addEventListener('DOMContentLoaded', function() {
    // Add styles for notifications
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 4px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            animation: slideIn 0.5s ease-out;
        }
        .notification.success {
            background-color: #28a745;
        }
        .notification.error {
            background-color: #dc3545;
        }
        @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }
    `;
    document.head.appendChild(style);

    // Function to show notifications
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
            const bookId = this.dataset.bookId;
            const bookElement = this.closest('.book');
            
            const userConfirmed = confirm('Are you sure you want to delete this book?');
            if (userConfirmed) {
                // Show loading state
                this.disabled = true;
                this.textContent = 'Deleting...';

                fetch(`delete/${bookId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrf_token')
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Remove the book element from the DOM with animation
                        bookElement.style.transition = 'opacity 0.5s ease-out';
                        bookElement.style.opacity = '0';
                        setTimeout(() => {
                            bookElement.remove();
                        }, 500);
                        showNotification('Book deleted successfully');
                    } else {
                        showNotification(data.message || 'Failed to delete book', 'error');
                        // Reset button state
                        this.disabled = false;
                        this.textContent = 'Delete';
                    }
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                    showNotification('Failed to delete book. Please try again.', 'error');
                    // Reset button state
                    this.disabled = false;
                    this.textContent = 'Delete';
                });
            }
        });
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}