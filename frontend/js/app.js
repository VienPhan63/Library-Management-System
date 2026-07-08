const APP_API_BASE = location.protocol === "file:" ? "http://127.0.0.1:8000" : "";

function authHeaders() {
  const token =
    localStorage.getItem("token") ||
    localStorage.getItem("librarian_token") ||
    localStorage.getItem("librarian_id");

  return token
    ? {
        Authorization: `Bearer ${token}`,
        "X-Librarian-Id": token,
      }
    : {};
}

function apiJsonHeaders() {
  return {
    "Content-Type": "application/json",
    ...authHeaders(),
  };
}

function formatNumber(value) {
  return Number(value || 0).toLocaleString("en-US");
}

function formatCurrency(value) {
  return `${Number(value || 0).toLocaleString("vi-VN")} VND`;
}

function formatDate(value) {
  if (!value) return "-";
  const date = new Date(`${value}T00:00:00`);
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleDateString("en-US", {
        month: "2-digit",
        day: "2-digit",
        year: "numeric",
      });
}

function toISODate(date) {
  return date.toISOString().slice(0, 10);
}

async function fetchJson(url, options = {}) {
  const response = await fetch(`${APP_API_BASE}${url}`, options);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return response.json();
}

function setupOperationsScreens() {
  const bookView = document.querySelector("#bookCatalogView");
  const categoryView = document.querySelector("#categoryView");
  const showCategory = document.querySelector("#showCategoryView");
  const showBooks = document.querySelector("#showBookView");

  showCategory?.addEventListener("click", () => {
    bookView?.classList.add("hidden");
    categoryView?.classList.remove("hidden");
  });

  showBooks?.addEventListener("click", () => {
    categoryView?.classList.add("hidden");
    bookView?.classList.remove("hidden");
  });
}

function setupBorrowBooksPage() {
  const readerInput = document.querySelector("#borrowReaderInput");
  const readerButton = document.querySelector("#borrowReaderSearch");
  const readerInfo = document.querySelector("#borrowReaderInfo");
  const bookInput = document.querySelector("#borrowBookInput");
  const bookButton = document.querySelector("#borrowBookSearch");
  const bookResults = document.querySelector("#borrowBookResults");
  const selectedTable = document.querySelector("#borrowSelectedTable");
  const selectedCount = document.querySelector("#borrowSelectedCount");
  const clearAllButton = document.querySelector("#borrowClearAll");
  const borrowDateInput = document.querySelector("#borrowDate");
  const dueDateInput = document.querySelector("#borrowDueDate");
  const receiptReader = document.querySelector("#borrowReceiptReader");
  const receiptItems = document.querySelector("#borrowReceiptItems");
  const receiptTotal = document.querySelector("#borrowReceiptTotal");
  const receiptStatus = document.querySelector("#borrowReceiptStatus");
  const receiptId = document.querySelector("#borrowReceiptId");
  const createButton = document.querySelector("#borrowCreateReceipt");
  const message = document.querySelector("#borrowMessage");

  if (!readerInput || !bookInput || !selectedTable) return;

  const today = new Date();
  const dueDate = new Date(today);
  dueDate.setDate(today.getDate() + 14);
  borrowDateInput.value = toISODate(today);
  dueDateInput.value = toISODate(dueDate);
  message?.classList.add("hidden");

  let selectedReader = null;
  let selectedBooks = [];

  function showBorrowMessage(text, isError = false) {
    if (!message) return;
    message.textContent = text;
    message.style.background = isError ? "#ffe1e1" : "#bdf0dd";
    message.style.color = isError ? "#a12828" : "#2f724f";
    message.classList.remove("hidden");
  }

  function renderReader(reader, summary = {}) {
    if (!readerInfo) return;
    const active = String(reader.card_status || reader.status) === "ACTIVE";
    readerInfo.innerHTML = `
      <div><strong>${reader.full_name || "-"}</strong><span class="ops-pill ${active ? "soft" : "red"}">${reader.card_status || reader.status || "-"}</span></div>
      <p>Card ID: ${reader.card_code || reader.id || "-"}</p>
      <p>Books currently borrowed: ${summary.currently_borrowed || 0}</p>
      <b>Overdue books: ${summary.overdue_books || 0}</b>
    `;
    receiptReader.textContent = `Valid card - Reader: ${reader.full_name || "-"} | ${reader.card_code || reader.id}`;
  }

  function renderSelectedBooks() {
    selectedCount.textContent = `${selectedBooks.length} books selected`;
    receiptTotal.textContent = selectedBooks.length;

    if (!selectedBooks.length) {
      selectedTable.innerHTML = '<tr><td colspan="4" style="text-align:center;">No books selected.</td></tr>';
      receiptItems.innerHTML = '<div class="loan-item"><strong>No books selected</strong><span>Due<br>-</span></div>';
      return;
    }

    selectedTable.innerHTML = selectedBooks
      .map(
        (book) => `
          <tr>
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td><button class="ops-icon danger" type="button" data-remove-book="${book.id}">Remove</button></td>
          </tr>
        `,
      )
      .join("");

    receiptItems.innerHTML = selectedBooks
      .map(
        (book) => `
          <div class="loan-item"><strong>${book.id}<br>${book.title}</strong><span>Due<br>${formatDate(dueDateInput.value)}</span></div>
        `,
      )
      .join("");
  }

  async function loadReader() {
    const readerId = readerInput.value.trim();
    if (!readerId) return;

    try {
      const reader = await fetchJson(`/readers/${encodeURIComponent(readerId)}`, {
        headers: authHeaders(),
      });
      const summary = await fetchJson(
        `/borrow-records/summary?reader_id=${encodeURIComponent(reader.id)}`,
      );
      selectedReader = reader;
      renderReader(reader, summary);
    } catch (error) {
      selectedReader = null;
      showBorrowMessage("Cannot load reader. Check librarian login/token and card ID.", true);
    }
  }

  async function searchBooks() {
    const keyword = bookInput.value.trim();
    try {
      const books = await fetchJson(`/books/search/?keyword=${encodeURIComponent(keyword)}`);
      const availableBooks = books.filter((book) => Number(book.available_quantity || 0) > 0);

      if (!availableBooks.length) {
        bookResults.innerHTML = '<div class="loan-mini-book"><div><strong>No available books found</strong><p>Try another keyword.</p><span class="ops-pill red">Unavailable</span></div><button type="button" disabled>+</button></div>';
        return;
      }

      bookResults.innerHTML = availableBooks
        .slice(0, 8)
        .map(
          (book) => `
            <div class="loan-mini-book">
              <div><strong>${book.title}</strong><p>Author: ${book.author} | ID: ${book.id}</p><span class="ops-pill soft">In Stock: ${book.available_quantity}</span></div>
              <button type="button" data-add-book="${book.id}">+</button>
            </div>
          `,
        )
        .join("");

      bookResults.querySelectorAll("[data-add-book]").forEach((button) => {
        button.addEventListener("click", () => {
          const book = availableBooks.find((item) => item.id === button.dataset.addBook);
          if (book && !selectedBooks.some((item) => item.id === book.id)) {
            selectedBooks.push(book);
            renderSelectedBooks();
          }
        });
      });
    } catch (error) {
      showBorrowMessage("Cannot search books from database.", true);
    }
  }

  async function createBorrowRecords() {
    if (!selectedReader) {
      showBorrowMessage("Please verify a reader before creating receipt.", true);
      return;
    }
    if (!selectedBooks.length) {
      showBorrowMessage("Please add at least one book.", true);
      return;
    }

    try {
      const created = [];
      for (const book of selectedBooks) {
        const result = await fetchJson("/borrow-records/", {
          method: "POST",
          headers: apiJsonHeaders(),
          body: JSON.stringify({
            reader_id: selectedReader.card_code || selectedReader.id,
            book_id: book.id,
            borrow_date: borrowDateInput.value,
            due_date: dueDateInput.value,
          }),
        });
        created.push(result.record?.id || result.record?.book_id || book.id);
      }

      receiptId.value = created.join(", ");
      receiptStatus.textContent = "Saved";
      receiptStatus.className = "ops-pill soft";
      selectedBooks = [];
      renderSelectedBooks();
      showBorrowMessage("Success! Borrow records were saved to database.");
    } catch (error) {
      showBorrowMessage("Cannot create borrow receipt. Check librarian login/token.", true);
    }
  }

  readerButton?.addEventListener("click", loadReader);
  readerInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") loadReader();
  });
  bookButton?.addEventListener("click", searchBooks);
  bookInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") searchBooks();
  });
  selectedTable.addEventListener("click", (event) => {
    const button = event.target.closest("[data-remove-book]");
    if (!button) return;
    selectedBooks = selectedBooks.filter((book) => book.id !== button.dataset.removeBook);
    renderSelectedBooks();
  });
  clearAllButton?.addEventListener("click", () => {
    selectedBooks = [];
    renderSelectedBooks();
  });
  dueDateInput.addEventListener("change", renderSelectedBooks);
  createButton?.addEventListener("click", createBorrowRecords);
}

function setupReturnBooksPage() {
  const readerInput = document.querySelector("#returnReaderInput");
  const readerButton = document.querySelector("#returnReaderSearch");
  const readerInfo = document.querySelector("#returnReaderInfo");
  const receiptInput = document.querySelector("#returnReceiptInput");
  const receiptButton = document.querySelector("#returnReceiptSearch");
  const receiptPreview = document.querySelector("#returnReceiptPreview");
  const table = document.querySelector("#returnRecordsTable");
  const count = document.querySelector("#returnConditionCount");
  const overdueFee = document.querySelector("#returnOverdueFee");
  const selectedTotal = document.querySelector("#returnSelectedTotal");
  const totalFine = document.querySelector("#returnTotalFine");
  const confirmButton = document.querySelector("#returnConfirmButton");
  const message = document.querySelector("#returnMessage");

  if (!readerInput || !table) return;

  let records = [];

  function estimateRecordFine(record) {
    const condition = document.querySelector(`[data-condition-for="${record.id}"]`)?.value || "NORMAL";
    const overdue = Number(record.fine_amount || 0);
    if (condition === "DAMAGED") return overdue + Number(record.book_price || 0) * 0.5;
    if (condition === "LOST") return overdue + Number(record.book_price || 0) * 2;
    return overdue;
  }

  function renderReader(reader, summary = {}) {
    const active = String(reader.card_status || reader.status) === "ACTIVE";
    readerInfo.innerHTML = `
      <div><strong>${reader.full_name || "-"}</strong><span class="ops-pill ${active ? "soft" : "red"}">${reader.card_status || reader.status || "-"}</span></div>
      <p>Card ID: ${reader.card_code || reader.id || "-"}</p>
      <p>Books currently borrowed: ${summary.currently_borrowed || 0}</p>
      <b>Overdue books: ${summary.overdue_books || 0}</b>
    `;
  }

  function updateReturnSummary() {
    const selected = records.filter((record) => {
      const checkbox = document.querySelector(`[data-return-record="${record.id}"]`);
      return checkbox?.checked;
    });
    const overdue = selected.reduce((sum, record) => sum + Number(record.fine_amount || 0), 0);
    const total = selected.reduce((sum, record) => sum + estimateRecordFine(record), 0);

    overdueFee.textContent = formatCurrency(overdue);
    selectedTotal.textContent = selected.length;
    totalFine.textContent = formatCurrency(total);
  }

  function renderRecords(list) {
    records = list.filter((record) => record.status === "BORROWED" || record.status === "OVERDUE");
    count.textContent = `Confirm condition and calculate fees for ${records.length} books.`;

    if (!records.length) {
      table.innerHTML = '<tr><td colspan="6" style="text-align:center;">No active borrow records found.</td></tr>';
      updateReturnSummary();
      return;
    }

    table.innerHTML = records
      .map((record) => {
        const statusClass = record.status === "OVERDUE" || Number(record.fine_amount || 0) > 0 ? "red" : "gray";
        const statusText = statusClass === "red" ? "Overdue" : "On Time";
        return `
          <tr>
            <td><label><input type="checkbox" data-return-record="${record.id}" checked> <strong>${record.book_title || record.book_id}</strong></label><br>${record.book_id}<br><small>${record.id}</small></td>
            <td>${formatDate(record.borrow_date)}</td>
            <td>${formatDate(record.due_date)}</td>
            <td><span class="ops-pill ${statusClass}">${statusText}</span></td>
            <td>
              <select data-condition-for="${record.id}">
                <option value="NORMAL">Normal</option>
                <option value="DAMAGED">Damaged</option>
                <option value="LOST">Lost</option>
              </select>
            </td>
            <td>${formatCurrency(record.fine_amount)}</td>
          </tr>
        `;
      })
      .join("");

    table.querySelectorAll("input, select").forEach((node) => {
      node.addEventListener("change", updateReturnSummary);
    });
    updateReturnSummary();
  }

  async function loadReaderReturns() {
    const readerId = readerInput.value.trim();
    if (!readerId) return;

    try {
      const reader = await fetchJson(`/readers/${encodeURIComponent(readerId)}`, {
        headers: authHeaders(),
      });
      const summary = await fetchJson(
        `/borrow-records/summary?reader_id=${encodeURIComponent(reader.id)}`,
      );
      renderReader(reader, summary);

      const activeRecords = await fetchJson(
        `/borrow-records/active?reader_id=${encodeURIComponent(reader.card_code || reader.id)}`,
        { headers: authHeaders() },
      );
      renderRecords(activeRecords);
    } catch (error) {
      message.textContent = "Cannot load reader return records. Check librarian login/token and card ID.";
    }
  }

  async function loadReceipt() {
    const recordId = receiptInput.value.trim();
    if (!recordId) return;

    try {
      const record = await fetchJson(`/borrow-records/${encodeURIComponent(recordId)}`);
      receiptPreview.innerHTML = `<span>#</span><div><strong>${record.book_title || record.book_id}</strong><p>Book ID: ${record.book_id}</p><p>Borrowed Date: ${formatDate(record.borrow_date)}</p></div>`;
      renderRecords([record]);
    } catch (error) {
      message.textContent = "Cannot find that borrow record.";
    }
  }

  async function confirmReturns() {
    const selected = records.filter((record) => {
      const checkbox = document.querySelector(`[data-return-record="${record.id}"]`);
      return checkbox?.checked;
    });

    if (!selected.length) {
      message.textContent = "Please select at least one borrow record.";
      return;
    }

    try {
      for (const record of selected) {
        const condition = document.querySelector(`[data-condition-for="${record.id}"]`)?.value || "NORMAL";
        await fetchJson(`/borrow-records/${encodeURIComponent(record.id)}/return`, {
          method: "PATCH",
          headers: apiJsonHeaders(),
          body: JSON.stringify({
            borrow_record_id: record.id,
            book_condition: condition,
            is_damaged: condition === "DAMAGED",
            is_lost: condition === "LOST",
            return_date: toISODate(new Date()),
          }),
        });
      }

      message.textContent = "Return processed successfully and database was updated.";
      renderRecords(records.filter((record) => !selected.some((item) => item.id === record.id)));
    } catch (error) {
      message.textContent = "Cannot confirm return. Check librarian login/token.";
    }
  }

  readerButton?.addEventListener("click", loadReaderReturns);
  readerInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") loadReaderReturns();
  });
  receiptButton?.addEventListener("click", loadReceipt);
  receiptInput?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") loadReceipt();
  });
  confirmButton?.addEventListener("click", confirmReturns);
}

function setupReportsPage() {
  const statNodes = document.querySelectorAll("[data-stat]");
  const startInput = document.querySelector("#reportStartDate");
  const endInput = document.querySelector("#reportEndDate");
  const filterButton = document.querySelector("#filterReports");
  const refreshButton = document.querySelector("#refreshReports");
  const detailButton = document.querySelector("#viewReportDetails");
  const detailsCard = document.querySelector("#reportDetailsCard");
  const detailsTable = document.querySelector("#reportDetailsTable");
  const detailsSummary = document.querySelector("#reportDetailsSummary");

  if (!statNodes.length) return;

  let currentStats = {};

  function renderDetails(stats) {
    const rows = [
      ["Total Books", stats.total_books],
      ["Borrowed Books", stats.borrowed_books],
      ["Total Borrows", stats.total_borrows],
      ["Total Returns", stats.total_returns],
      ["Overdue Returns", stats.overdue_returns],
      ["Total Fine Amount", formatCurrency(stats.total_fine_amount)],
      ["Total Cards Issued", stats.total_cards_issued],
      ["Active Readers", stats.active_readers],
      ["Most Borrowed Book", stats.most_borrowed_book ? `${stats.most_borrowed_book.title} (${stats.most_borrowed_book.times})` : "-"],
      ["Most Active Reader", stats.most_active_reader ? `${stats.most_active_reader.full_name} (${stats.most_active_reader.times})` : "-"],
    ];

    detailsTable.innerHTML = rows
      .map(([label, value]) => `<tr><td>${label}</td><td>${value ?? 0}</td></tr>`)
      .join("");
    detailsSummary.textContent = "Loaded from /reports/summary";
  }

  function renderStats(stats) {
    currentStats = stats;
    statNodes.forEach((node) => {
      const value = stats[node.dataset.stat] ?? 0;
      node.textContent =
        node.dataset.format === "currency" ? formatCurrency(value) : formatNumber(value);
    });

    const borrowedNote = document.querySelector('[data-stat-note="borrowed_books"]');
    if (borrowedNote) {
      const total = Number(stats.total_books || 0);
      const borrowed = Number(stats.borrowed_books || 0);
      const percent = total ? ((borrowed / total) * 100).toFixed(1) : "0.0";
      borrowedNote.textContent = `${percent}% of total titles`;
    }

    const returnsNote = document.querySelector('[data-stat-note="total_returns"]');
    if (returnsNote) {
      const totalBorrows = Number(stats.total_borrows || 0);
      const totalReturns = Number(stats.total_returns || 0);
      const percent = totalBorrows ? ((totalReturns / totalBorrows) * 100).toFixed(1) : "0.0";
      returnsNote.textContent = `${percent}% completion rate`;
    }

    if (!detailsCard.classList.contains("hidden")) renderDetails(stats);
  }

  async function loadDatabaseStatistics() {
    const params = new URLSearchParams();
    if (startInput?.value) params.set("start_date", startInput.value);
    if (endInput?.value) params.set("end_date", endInput.value);
    const query = params.toString() ? `?${params.toString()}` : "";

    try {
      const stats = await fetchJson(`/reports/summary${query}`, {
        headers: authHeaders(),
      });
      renderStats(stats);
    } catch (error) {
      detailsCard?.classList.remove("hidden");
      detailsTable.innerHTML =
        '<tr><td colspan="2" style="text-align:center;">Cannot load report data. Check librarian login/token.</td></tr>';
    }
  }

  filterButton?.addEventListener("click", loadDatabaseStatistics);
  refreshButton?.addEventListener("click", loadDatabaseStatistics);
  detailButton?.addEventListener("click", () => {
    detailsCard?.classList.toggle("hidden");
    if (!detailsCard.classList.contains("hidden")) renderDetails(currentStats);
  });

  loadDatabaseStatistics();
}

setupOperationsScreens();
setupBorrowBooksPage();
setupReturnBooksPage();
setupReportsPage();
