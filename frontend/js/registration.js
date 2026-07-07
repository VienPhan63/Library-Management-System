let currentRequest = null;

function showPage(pageId) {
  ["listPage", "detailPage", "successPage"].forEach((id) => {
    const page = document.getElementById(id);
    if (page) page.classList.toggle("hidden", id !== pageId);
  });
}

function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

async function loadPendingRegistrations() {
  const tbody = document.getElementById("registrationTable");
  const count = document.getElementById("pendingCount");
  if (!tbody) return;

  try {
    const registrations = await requestJson("/registrations/pending");

    tbody.innerHTML = registrations.map((request) => `
      <tr>
        <td>${escapeHtml(request.id)}</td>
        <td>${escapeHtml(request.full_name)}</td>
        <td>${escapeHtml(request.email)}</td>
        <td>${escapeHtml(request.phone_number)}</td>
        <td><span class="status borrowed">${escapeHtml(request.status)}</span></td>
        <td><button class="outline-btn small" type="button" data-request-id="${escapeHtml(request.id)}">View</button></td>
      </tr>
    `).join("");

    if (!registrations.length) {
      tbody.innerHTML = `<tr><td colspan="6">No pending registrations.</td></tr>`;
    }

    if (count) count.textContent = `${registrations.length} requests`;
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="6">${escapeHtml(error.message)}</td></tr>`;
    if (count) count.textContent = "0 requests";
  }
}

function renderDetail(request) {
  currentRequest = request;

  document.getElementById("detailStatus").textContent = request.status;
  document.getElementById("detailCreatedAt").textContent = formatDate(request.request_date);
  document.getElementById("detailName").textContent = request.full_name;
  document.getElementById("detailNameInfo").textContent = request.full_name;
  document.getElementById("detailInitial").textContent = request.full_name.trim().charAt(0).toUpperCase() || "R";
  document.getElementById("detailRequestId").textContent = `Request ID: ${request.id}`;
  document.getElementById("detailEmail").textContent = request.email;
  document.getElementById("detailPhone").textContent = request.phone_number;
  document.getElementById("detailGender").textContent = request.gender;
  document.getElementById("detailDateOfBirth").textContent = request.date_of_birth || "-";
  document.getElementById("detailNationalId").textContent = request.national_id || "-";
  document.getElementById("verifyMessage").textContent = "";

  showPage("detailPage");
}

async function openRequestDetail(requestId) {
  const request = await requestJson(`/registrations/${encodeURIComponent(requestId)}`);
  renderDetail(request);
}

function renderSuccess(request) {
  const isApproved = request.status === "APPROVED";
  const status = document.getElementById("successStatus");
  const tabs = document.querySelectorAll(".reg-tabs button");

  document.getElementById("successTitle").textContent = isApproved
    ? "Approval Processed Successfully"
    : "Rejection Processed Successfully";

  status.textContent = request.status;
  status.className = `reg-status ${isApproved ? "approved" : "rejected"}`;

  tabs.forEach((tab, index) => {
    tab.classList.toggle("active", isApproved ? index === 0 : index === 1);
  });

  document.getElementById("successMessage").textContent = isApproved
    ? `Approved: The library card has been issued to ${request.full_name}.`
    : `Rejected: ${request.rejection_reason}`;

  showPage("successPage");
}

async function approveCurrentRequest() {
  if (!currentRequest) return;

  const request = await requestJson(
    `/registrations/${encodeURIComponent(currentRequest.id)}/approve`,
    { method: "PATCH" }
  );

  renderSuccess(request);
}

async function rejectCurrentRequest() {
  if (!currentRequest) return;

  const reason = prompt("Enter rejection reason:");
  if (!reason || !reason.trim()) return;

  const request = await requestJson(
    `/registrations/${encodeURIComponent(currentRequest.id)}/reject`,
    {
      method: "PATCH",
      body: JSON.stringify({ reason })
    }
  );

  renderSuccess(request);
}

document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("registrationTable");

  table?.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-request-id]");
    if (!button) return;

    try {
      await openRequestDetail(button.dataset.requestId);
    } catch (error) {
      alert(error.message);
    }
  });

  document.getElementById("backToList")?.addEventListener("click", () => {
    showPage("listPage");
  });

  document.getElementById("successBackBtn")?.addEventListener("click", async () => {
    showPage("listPage");
    await loadPendingRegistrations();
  });

  document.getElementById("approveBtn")?.addEventListener("click", async () => {
    try {
      await approveCurrentRequest();
    } catch (error) {
      alert(error.message);
    }
  });

  document.getElementById("rejectBtn")?.addEventListener("click", async () => {
    try {
      await rejectCurrentRequest();
    } catch (error) {
      alert(error.message);
    }
  });

  loadPendingRegistrations();
});
