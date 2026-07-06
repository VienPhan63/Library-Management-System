const BASE_URL = "http://127.0.0.1:8000";

function displayBooks(books) {
    const bookList = document.getElementById("bookList");

    bookList.innerHTML = "";

    if (books.length === 0) {
        bookList.innerHTML = "<p>Không tìm thấy sách nào.</p>";
        return;
    }

    books.forEach(book => {
        const statusClass = book.status === "available"
            ? "status-available"
            : "status-borrowed";

        const bookCard = `
            <div class="book-card">
                <h3>${book.title}</h3>
                <p><strong>ID:</strong> ${book.id}</p>
                <p><strong>Author:</strong> ${book.author}</p>
                <p><strong>Category:</strong> ${book.category}</p>
                <p><strong>Status:</strong> <span class="${statusClass}">${book.status}</span></p>
                <p><strong>Description:</strong> ${book.description}</p>
            </div>
        `;

        bookList.innerHTML += bookCard;
    });
}

async function loadBooks() {
    const response = await fetch(`${BASE_URL}/books`);
    const books = await response.json();

    displayBooks(books);
}

async function searchBooks() {
    const keyword = document.getElementById("keywordInput").value;

    const response = await fetch(`${BASE_URL}/books/search/?keyword=${keyword}`);
    const books = await response.json();

    displayBooks(books);
}