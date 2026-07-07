
const registerForm = document.querySelector("#registerForm");

function setError(input, message) {
  const group = input.closest(".form-group");
  const error = group ? group.querySelector(".error") : null;
  if (error) error.textContent = message;
}

function clearErrors() {
  document.querySelectorAll(".error").forEach((error) => {
    error.textContent = "";
  });
}

registerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  clearErrors();

  const requiredFields = [
    fullName, dob, gender, idNumber, phone, email, password, confirmPassword
  ];

  let isValid = true;

  requiredFields.forEach((field) => {
    if (!field.value.trim()) {
      setError(field, "This field is required.");
      isValid = false;
    }
  });

  if (email.value && !email.value.includes("@")) {
    setError(email, "Email is invalid.");
    isValid = false;
  }

  if (password.value && password.value.length < 6) {
    setError(password, "Password must be at least 6 characters.");
    isValid = false;
  }

  if (password.value !== confirmPassword.value) {
    setError(confirmPassword, "Confirm password does not match.");
    isValid = false;
  }

  if (!agree.checked) {
    document.querySelector("#agreeError").textContent = "Please agree before submitting.";
    isValid = false;
  }

  if (!isValid) return;

  alert("Registration submitted successfully! Please wait for librarian approval.");
  window.location.href = "login.html";
});
