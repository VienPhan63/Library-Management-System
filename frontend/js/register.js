async function register() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;
  const agreeTerms = document.getElementById("agree_terms").checked;

  if (password !== confirmPassword) {
    alert("Password and confirm password do not match.");
    return;
  }

  if (!agreeTerms) {
    alert("Please agree to the library card terms of use.");
    return;
  }

  const data = {
    full_name: document.getElementById("full_name").value.trim(),
    email: document.getElementById("email").value.trim(),
    password,
    phone_number: document.getElementById("phone_number").value.trim(),
    gender: document.getElementById("gender").value,
    date_of_birth: document.getElementById("date_of_birth").value || null,
    national_id: document.getElementById("national_id").value.trim() || null,
  };

  const response = await fetch("/registrations/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (response.ok) {
    alert("Register successfully! Your request is pending librarian approval.");
    document.getElementById("registerForm").reset();
  } else {
    alert(result.detail || "Register failed.");
  }
}

document
  .getElementById("registerForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    await register();
  });
