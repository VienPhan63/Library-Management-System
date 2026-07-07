async function register() {
  const data = {
    full_name: document.getElementById("full_name").value,

    email: document.getElementById("email").value,

    password: document.getElementById("password").value,

    phone_number: document.getElementById("phone_number").value,

    gender: document.getElementById("gender").value,
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
    alert("Register successfully!");
  } else {
    alert(result.detail);
  }
}
