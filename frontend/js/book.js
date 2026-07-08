const BASE_URL = "http://127.0.0.1:8000";

function displayBooks(books) {
  const bookList = document.getElementById("bookList");

  if (!bookList) return;
  bookList.innerHTML = "";

  if (!Array.isArray(books) || books.length === 0) {
    bookList.innerHTML = "<p>Không tìm thấy sách nào.</p>";
    return;
  }

  books.forEach((book) => {
    const statusClass =
      book.status === "available" ? "status-available" : "status-borrowed";

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

function renderManageBooks(books) {
  const tbody = document.getElementById("manageBooksTable");
  if (!tbody) return;

  if (!Array.isArray(books) || books.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="9" style="text-align:center;">No books found.</td></tr>';
  } else {
    tbody.innerHTML = books
      .map((book) => {
        const quantity = Number(book.available_quantity ?? book.quantity ?? 0);
        const isAvailable = quantity > 0;
        const statusText = isAvailable ? "Available" : "In Stock";
        const badgeClass = isAvailable ? "green" : "red";

        return `
                <tr data-book-id="${book.id || ""}">
                    <td>${book.id || "-"}</td>
                    <td>${book.title || "-"}</td>
                    <td>${book.author || "-"}</td>
                    <td>${book.publisher || "-"}</td>
                    <td>${book.publish_year || "-"}</td>
                    <td><span class="ops-tag">${book.category || "-"}</span></td>
                    <td>${quantity}</td>
                    <td><span class="ops-pill ${badgeClass}">${statusText}</span></td>
                    <td>
                        <button class="ops-icon" type="button" data-edit-book>Edit</button>
                        <button class="ops-icon" type="button">Delete</button>
                    </td>
                </tr>
            `;
      })
      .join("");
  }

  document.querySelectorAll('[data-stat="total_titles"]').forEach((node) => {
    node.textContent = Array.isArray(books) ? books.length : 0;
  });

  const categories = Array.isArray(books)
    ? new Set(books.map((book) => book.category).filter(Boolean)).size
    : 0;

  document
    .querySelectorAll('[data-stat="total_categories"]')
    .forEach((node) => {
      node.textContent = categories;
    });

  tbody.querySelectorAll("[data-edit-book]").forEach((button) => {
    button.addEventListener("click", () => handleEditBookClick(button));
  });
}

function populateBookEditor(book) {
  const editor = document.getElementById("bookEditor");
  const title = document.getElementById("bookEditorTitle");
  const form = document.getElementById("bookForm");
  const bookId = document.getElementById("bookId");
  const titleInput = document.getElementById("bookTitle");
  const authorInput = document.getElementById("bookAuthor");
  const categoryInput = document.getElementById("bookCategory");
  const descriptionInput = document.getElementById("bookDescription");
  const publisherInput = document.getElementById("bookPublisher");
  const publishYearInput = document.getElementById("bookPublishYear");
  const quantityInput = document.getElementById("bookQuantity");
  const availableQuantityInput = document.getElementById(
    "bookAvailableQuantity",
  );
  const priceInput = document.getElementById("bookPrice");
  const statusInput = document.getElementById("bookStatus");
  const librarianIdInput = document.getElementById("librarianId");

  if (!form || !editor) return;

  if (book) {
    title.textContent = "Edit Book";
    bookId.value = book.id || "";
    titleInput.value = book.title || "";
    authorInput.value = book.author || "";
    categoryInput.value = book.category || "";
    descriptionInput.value = book.description || "";
    publisherInput.value = book.publisher || "";
    publishYearInput.value = book.publish_year || "";
    quantityInput.value = book.quantity ?? "";
    availableQuantityInput.value = book.available_quantity ?? "";
    priceInput.value = book.price ?? "";
    statusInput.value = book.status || "AVAILABLE";
    librarianIdInput.value = book.librarian_id || "";
  } else {
    title.textContent = "Add New Book";
    form.reset();
    bookId.value = "";
    librarianIdInput.value = "";
  }

  editor.classList.remove("hidden");
}

function handleEditBookClick(button) {
  const row = button.closest("tr");
  const books = window.__loadedBooks || [];
  const rowIndex = Array.from(row?.parentElement?.children || []).indexOf(row);
  const selectedBook = books[rowIndex];

  if (selectedBook) {
    populateBookEditor(selectedBook);
  }
}

async function submitBookForm(event) {
  event.preventDefault();

  const form = document.getElementById("bookForm");
  if (!form) return;

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  payload.quantity = Number(payload.quantity);
  payload.available_quantity = Number(payload.available_quantity);
  payload.publish_year = Number(payload.publish_year);
  payload.price = Number(payload.price);

  const bookId = payload.book_id;
  const url = `${BASE_URL}/books${bookId ? `/${bookId}` : "/"}`;
  const method = bookId ? "PUT" : "POST";

  const response = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Book save failed", errorText);
    alert("Failed to save book");
    return;
  }

  const toast = document.getElementById("bookToast");
  toast?.classList.remove("hidden");
  window.setTimeout(() => toast?.classList.add("hidden"), 2200);
  form.reset();
  await loadBooks();
}

function bindManageBookActions() {
  const table = document.getElementById("manageBooksTable");
  const form = document.getElementById("bookForm");
  const openEditorButton = document.getElementById("openBookEditor");
  const closeEditorButton = document.getElementById("closeBookEditor");
  const cancelEditorButton = document.getElementById("cancelBookEditor");
  const editor = document.getElementById("bookEditor");

  if (!table) return;

  table.addEventListener("click", (event) => {
    const button = event.target.closest("[data-edit-book]");
    if (!button) return;

    handleEditBookClick(button);
  });

  openEditorButton?.addEventListener("click", () => populateBookEditor(null));
  closeEditorButton?.addEventListener("click", () =>
    editor?.classList.add("hidden"),
  );
  cancelEditorButton?.addEventListener("click", () =>
    editor?.classList.add("hidden"),
  );
  form?.addEventListener("submit", submitBookForm);
}

async function loadBooks() {
  const response = await fetch(`${BASE_URL}/books/`);
  if (!response.ok) {
    throw new Error(`Failed to load books: ${response.status}`);
  }

  const books = await response.json();

  window.__loadedBooks = books;

  if (document.getElementById("manageBooksTable")) {
    renderManageBooks(books);
  } else {
    displayBooks(books);
  }

  return books;
}

async function searchBooks() {
  const keyword = document.getElementById("keywordInput").value;

  const response = await fetch(`${BASE_URL}/books/search/?keyword=${keyword}`);
  const books = await response.json();

  displayBooks(books);
}

document.addEventListener("DOMContentLoaded", () => {
  bindManageBookActions();

  if (
    document.getElementById("manageBooksTable") ||
    document.getElementById("bookList")
  ) {
    loadBooks().catch((error) => {
      console.error(error);
    });
  }
});
