const API_BASE = location.protocol === "file:" ? "http://127.0.0.1:8000" : "";

function formatDate(value) {
  if (!value) return "-- Pending --";
  const date = new Date(`${value}T00:00:00`);
  return date.toLocaleDateString("en-US", {
    month: "2-digit",
    day: "2-digit",
    year: "numeric",
  });
}

function formatMoney(value) {
  return `${Number(value || 0).toLocaleString("vi-VN")} VND`;
}

function setupReaderSearch() {
  const searchInput = document.querySelector("#bookSearchInput");
  const genreFilter = document.querySelector("#genreFilter");
  const statusFilter = document.querySelector("#statusFilter");
  const booksTable = document.querySelector("#booksTable");
  const resultCount = document.querySelector("#resultCount");

  if (!searchInput || !genreFilter || !statusFilter || !booksTable || !resultCount) {
    return;
  }

  let databaseBooks = [];

  function bookStatus(book) {
    const hasCopies = Number(book.available_quantity || 0) > 0;
    return book.status === "AVAILABLE" && hasCopies ? "available" : "borrowed";
  }

  function statusLabel(status) {
    return status === "available" ? "Available" : "Borrowed";
  }

  function renderBooks(list) {
    resultCount.textContent = `${list.length} results`;

    if (!list.length) {
      booksTable.innerHTML = '<tr><td colspan="8" class="empty-row">No books found.</td></tr>';
      return;
    }

    booksTable.innerHTML = list.map((book) => {
      const status = bookStatus(book);
      return `
        <tr>
          <td>${book.id}</td>
          <td>${book.title}</td>
          <td>${book.publisher}</td>
          <td>${book.author}</td>
          <td>${book.publish_year}</td>
          <td><span class="genre-tag">${book.category}</span></td>
          <td><span class="status ${status}">${statusLabel(status)}</span></td>
          <td>${book.description || ">"}</td>
        </tr>
      `;
    }).join("");
  }

  function applyFilters() {
    const keyword = searchInput.value.trim().toLowerCase();
    const genre = genreFilter.value;
    const status = statusFilter.value;

    const filtered = databaseBooks.filter((book) => {
      const searchable = [
        book.id,
        book.title,
        book.publisher,
        book.author,
        book.publish_year,
        book.category,
        book.description,
      ].join(" ").toLowerCase();

      return (!keyword || searchable.includes(keyword))
        && (!genre || book.category === genre)
        && (!status || bookStatus(book) === status);
    });

    renderBooks(filtered);
  }

  function populateGenres() {
    const genres = [...new Set(databaseBooks.map((book) => book.category).filter(Boolean))].sort();
    genreFilter.innerHTML = '<option value="">All genres</option>' + genres
      .map((genre) => `<option value="${genre}">${genre}</option>`)
      .join("");
  }

  async function loadBooks() {
    try {
      const response = await fetch(`${API_BASE}/books/search/?keyword=`);
      if (!response.ok) throw new Error("Could not load books");
      databaseBooks = await response.json();
      populateGenres();
      applyFilters();
    } catch (error) {
      booksTable.innerHTML = '<tr><td colspan="8" class="empty-row">Cannot connect to the database.</td></tr>';
    }
  }

  searchInput.addEventListener("input", applyFilters);
  genreFilter.addEventListener("change", applyFilters);
  statusFilter.addEventListener("change", applyFilters);
  loadBooks();
}

function setupBorrowingHistory() {
  const readerId = localStorage.getItem("reader_id") || "";
  const historyTable = document.querySelector("#historyTable");
  const historySearch = document.querySelector("#historySearch");
  const historyCount = document.querySelector("#historyCount");

  if (!historyTable || !historySearch || !historyCount) {
    return;
  }

  let historyRows = [];

  function historyStatusClass(status) {
    if (status === "RETURNED") return "returned";
    if (status === "OVERDUE") return "overdue";
    return "borrowed";
  }

  function historyStatusLabel(status) {
    if (status === "RETURNED") return "Returned";
    if (status === "OVERDUE") return "Overdue";
    return "Borrowed";
  }

  function renderHistory(list) {
    historyCount.textContent = `Showing ${list.length} records`;

    if (!list.length) {
      historyTable.innerHTML = '<tr><td colspan="7" class="empty-row">No borrowing records found.</td></tr>';
      return;
    }

    historyTable.innerHTML = list.map((row) => {
      const fineClass = Number(row.fine_amount || 0) > 0 ? "fine-danger" : "";
      return `
        <tr>
          <td>${row.id}</td>
          <td>${row.book_title || row.book_id}</td>
          <td>${formatDate(row.borrow_date)}</td>
          <td class="due-date">${formatDate(row.due_date)}</td>
          <td>${formatDate(row.return_date)}</td>
          <td class="${fineClass}">${formatMoney(row.fine_amount)}</td>
          <td><span class="status ${historyStatusClass(row.status)}">${historyStatusLabel(row.status)}</span></td>
        </tr>
      `;
    }).join("");
  }

  function applyHistoryFilter() {
    const keyword = historySearch.value.trim().toLowerCase();
    const filtered = historyRows.filter((row) => {
      const searchable = [
        row.id,
        row.book_id,
        row.book_title,
        row.borrow_date,
        row.due_date,
        row.return_date,
        row.status,
        row.fine_amount,
      ].join(" ").toLowerCase();
      return !keyword || searchable.includes(keyword);
    });
    renderHistory(filtered);
  }

  async function loadSummary() {
    const params = readerId ? `?reader_id=${encodeURIComponent(readerId)}` : "";
    const response = await fetch(`${API_BASE}/borrow-records/summary${params}`);
    if (!response.ok) return;

    const summary = await response.json();
    document.querySelector("#totalBorrows").textContent = summary.total_borrows || 0;
    document.querySelector("#currentBorrows").textContent = String(summary.currently_borrowed || 0).padStart(2, "0");
    document.querySelector("#overdueBooks").textContent = summary.overdue_books || 0;
    document.querySelector("#totalFines").textContent = formatMoney(summary.total_fines);
  }

  async function loadHistory() {
    try {
      const params = readerId ? `?reader_id=${encodeURIComponent(readerId)}` : "";
      const response = await fetch(`${API_BASE}/borrow-records/${params}`);
      if (!response.ok) throw new Error("Could not load borrowing records");
      historyRows = await response.json();
      applyHistoryFilter();
      loadSummary();
    } catch (error) {
      historyTable.innerHTML = '<tr><td colspan="7" class="empty-row">Cannot connect to the database.</td></tr>';
    }
  }

  historySearch.addEventListener("input", applyHistoryFilter);
  loadHistory();
}

setupReaderSearch();
setupBorrowingHistory();
