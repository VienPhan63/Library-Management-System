
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
  const passwordValue = password.value.trim();

  if (account === "librarian@librarian.com" && passwordValue === "librarianpassword") {
    window.location.href = "librarian-books.html";
  } else if (account === "reader@reader.com" && passwordValue === "readerpassword") {
    window.location.href = "reader-search.html";
  } else {
    passwordError.textContent = "Wrong username or password. Please try again.";
    password.value = "";
    password.focus();
  }
});
