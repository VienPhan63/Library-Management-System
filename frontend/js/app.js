
const books = [
  { code: "LT1001", title: "The Adventures of a Cricket", publisher: "Kim Dong Publisher", author: "To Hoai", year: 2023, genre: "Literature", status: "Borrowed", qty: 8 },
  { code: "FL002", title: "Business Chinese", publisher: "Education Publisher", author: "Yangchen", year: 2019, genre: "Foreign Language", status: "Available", qty: 40 },
  { code: "EC009", title: "Human Resource Management", publisher: "Alpha Books", author: "Mai Le Ha", year: 2018, genre: "Business", status: "Available", qty: 6 },
  { code: "T0009", title: "Python Programming", publisher: "Science Publisher", author: "Nguyen Van", year: 2020, genre: "Technology", status: "Available", qty: 10 },
  { code: "TC009", title: "Database Management System", publisher: "Science Publisher", author: "Vo Van Binh", year: 2023, genre: "Technology", status: "Available", qty: 18 }
];

const historyRows = [
  ["P-2026-001", "C++ Programming for Beginners", "01/02/2026", "15/02/2026", "15/02/2026", "0 ₫", "Returned"],
  ["BP-2026-018", "Modern User Interface Design", "01/03/2026", "15/03/2026", "Pending", "0 ₫", "Borrowing"],
  ["HC-2026-003", "Data Structures and Algorithms", "01/05/2026", "15/05/2026", "16/05/2026", "40.000 ₫", "Returned"],
  ["BP-2026-018", "Basic Python Programming", "10/05/2026", "24/05/2026", "Pending", "5.000 ₫", "Borrowing"],
  ["SA-2026-008", "The Psychology of Money", "05/06/2026", "19/06/2026", "20/06/2026", "5.000 ₫", "Returned"]
];

function setActiveNav() {
  const path = location.pathname.split("/").pop();
  document.querySelectorAll(".side-nav a").forEach((link) => {
    const href = link.getAttribute("href");
    if (href === path) link.classList.add("active");
  });

  if (path.includes("librarian") || path.includes("borrow") || path.includes("return")) {
    const roleText = document.querySelector("#roleText");
    const userRole = document.querySelector("#userRole");
    const userName = document.querySelector("#userName");
    if (roleText) roleText.textContent = "Librarian";
    if (userRole) userRole.textContent = "Librarian";
    if (userName) userName.textContent = "Tran Anh Thu";
  }
}

function renderReaderBooks(list = books) {
  const tbody = document.querySelector("#booksTable");
  const count = document.querySelector("#resultCount");
  if (!tbody) return;

  tbody.innerHTML = list.map(book => `
    <tr>
      <td>${book.code}</td>
      <td>${book.title}</td>
      <td>${book.publisher}</td>
      <td>${book.author}</td>
      <td>${book.year}</td>
      <td>${book.genre}</td>
      <td><span class="status ${book.status === "Available" ? "available" : "borrowed"}">${book.status}</span></td>
      <td>›</td>
    </tr>
  `).join("");

  if (count) count.textContent = `${list.length} books`;
}

function setupBookSearch() {
  const input = document.querySelector("#bookSearchInput");
  const genre = document.querySelector("#genreFilter");
  const status = document.querySelector("#categoryFilter");
  if (!input) return;

  function filterBooks() {
    const keyword = input.value.toLowerCase();
    const genreValue = genre.value;
    const statusValue = status.value;

    const filtered = books.filter(book => {
      const matchKeyword =
        book.title.toLowerCase().includes(keyword) ||
        book.author.toLowerCase().includes(keyword);
      const matchGenre = !genreValue || book.genre === genreValue;
      const matchStatus = !statusValue || book.status === statusValue;
      return matchKeyword && matchGenre && matchStatus;
    });

    renderReaderBooks(filtered);
  }

  input.addEventListener("input", filterBooks);
  genre.addEventListener("change", filterBooks);
  status.addEventListener("change", filterBooks);
  renderReaderBooks();
}

function renderHistory(list = historyRows) {
  const tbody = document.querySelector("#historyTable");
  if (!tbody) return;

  tbody.innerHTML = list.map(row => `
    <tr>
      ${row.slice(0,6).map(cell => `<td>${cell}</td>`).join("")}
      <td><span class="status ${row[6] === "Returned" ? "available" : "borrowed"}">${row[6]}</span></td>
    </tr>
  `).join("");
}

function setupHistorySearch() {
  const input = document.querySelector("#historySearch");
  if (!input) return;

  input.addEventListener("input", () => {
    const keyword = input.value.toLowerCase();
    const filtered = historyRows.filter(row => row.join(" ").toLowerCase().includes(keyword));
    renderHistory(filtered);
  });

  renderHistory();
}

function renderManageBooks() {
  const tbody = document.querySelector("#manageBooksTable");
  if (!tbody) return;

  tbody.innerHTML = books.map(book => `
    <tr>
      <td>${book.code}</td>
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td>${book.publisher}</td>
      <td>${book.year}</td>
      <td>${book.genre}</td>
      <td>${book.qty}</td>
      <td><span class="status ${book.status === "Available" ? "available" : "rejected"}">${book.status}</span></td>
      <td>✎ 🗑</td>
    </tr>
  `).join("");
}

function setupBookModal() {
  const modal = document.querySelector("#bookModal");
  const openBtn = document.querySelector("#openAddBook");
  const closeBtn = document.querySelector("#closeModal");
  const form = document.querySelector("#addBookForm");
  if (!modal || !openBtn) return;

  openBtn.addEventListener("click", () => modal.classList.add("show"));
  closeBtn.addEventListener("click", () => modal.classList.remove("show"));

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    books.push({
      code: newBookCode.value || "NEW001",
      title: newBookTitle.value || "New Book",
      publisher: "Science Publisher",
      author: newBookAuthor.value || "Unknown",
      year: new Date().getFullYear(),
      genre: newBookGenre.value,
      status: "Available",
      qty: Number(newBookQuantity.value || 1)
    });

    renderManageBooks();
    modal.classList.remove("show");
    form.reset();
  });

  renderManageBooks();
}

function setupApprovalButtons() {
  const approve = document.querySelector("#approveBtn");
  const reject = document.querySelector("#rejectBtn");
  const msg = document.querySelector("#verifyMessage");
  if (!approve) return;

  approve.addEventListener("click", () => {
    msg.textContent = "Status Approved: The library card has been issued.";
  });

  reject.addEventListener("click", () => {
    const reason = prompt("Enter rejection reason:");
    msg.textContent = reason ? `Status Rejected: ${reason}` : "Request rejected.";
  });
}

setActiveNav();
setupBookSearch();
setupHistorySearch();
setupBookModal();
setupApprovalButtons();
