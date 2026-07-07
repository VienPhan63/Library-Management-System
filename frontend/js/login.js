
const loginForm = document.querySelector("#loginForm");

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const username = document.querySelector("#username");
  const password = document.querySelector("#password");
  const usernameError = document.querySelector("#usernameError");
  const passwordError = document.querySelector("#passwordError");

  usernameError.textContent = "";
  passwordError.textContent = "";

  let isValid = true;

  if (username.value.trim() === "") {
    usernameError.textContent = "Please enter username or email.";
    isValid = false;
  }

  if (password.value.trim() === "") {
    passwordError.textContent = "Please enter password.";
    isValid = false;
  }

  if (!isValid) return;

  const account = username.value.trim().toLowerCase();

  if (account.includes("lib") || account.includes("admin")) {
    window.location.href = "librarian-books.html";
  } else {
    window.location.href = "reader-search.html";
  }
});
