function loadChapter(id) {
    fetch(`/chapter/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('content').innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById('content').innerHTML = data.content;
            }
        });
}

// Load the last read chapter on page load
document.addEventListener('DOMContentLoaded', () => {
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
