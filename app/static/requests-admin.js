const errorBox = document.querySelector("#requests-error");
const STATUSES = ["REQUESTED", "CONFIRMED", "READY", "COMPLETED", "CANCELLED"];
const OUTCOMES = ["", "HONOURED", "WRONG_FIT", "OUT_OF_STOCK", "PRICE_CHANGED", "NO_SHOW"];
const REQUEST_STATUSES = ["OPEN", "ANSWERED", "CLOSED"];

const cell = (text) => { const td = document.createElement("td"); td.textContent = text ?? "—"; return td; };
const date = (value) => (value ? new Date(value).toLocaleString("en-GB", { dateStyle: "short", timeStyle: "short" }) : "—");

function select(values, current) {
  const node = document.createElement("select");
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value; option.textContent = value ? value.replaceAll("_", " ").toLowerCase() : "—";
    node.append(option);
  });
  node.value = current || "";
  return node;
}

function showError(message) {
  errorBox.hidden = false;
  errorBox.textContent = message;
}

async function patch(url, body) {
  const response = await fetch(url, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!response.ok) showError("Saving failed. Reload the page and try again.");
  return response.ok;
}

async function loadReservations() {
  const response = await fetch("/api/admin/reservations");
  if (!response.ok) throw new Error("Reservations could not be loaded");
  const rows = await response.json();
  document.querySelector("#reservation-count").textContent = `${rows.length}`;
  document.querySelector("#reservation-rows").replaceChildren(...rows.map((row) => {
    const tr = document.createElement("tr");
    const status = select(STATUSES, row.status);
    const outcome = select(OUTCOMES, row.outcome);
    const save = document.createElement("button");
    save.type = "button"; save.textContent = "Save";
    save.addEventListener("click", async () => {
      if (await patch(`/api/admin/reservations/${row.id}`, { status: status.value, outcome: outcome.value || null })) save.textContent = "Saved";
    });
    const part = cell(`${row.product_name} (${row.product_id})`);
    tr.append(
      cell(date(row.created_at)),
      part,
      cell(`${row.supplier_name}${row.supplier_sku ? ` · ${row.supplier_sku}` : ""}`),
      cell(String(row.quantity)),
      cell(row.phone),
      cell([row.vehicle_label, row.vin].filter(Boolean).join(" · ") || null),
      cell(row.note),
    );
    [status, outcome, save].forEach((control) => { const td = document.createElement("td"); td.append(control); tr.append(td); });
    return tr;
  }));
}

async function loadPartRequests() {
  const response = await fetch("/api/admin/part-requests");
  if (!response.ok) throw new Error("Part requests could not be loaded");
  const rows = await response.json();
  document.querySelector("#request-count").textContent = `${rows.filter((row) => row.status === "OPEN").length} open`;
  document.querySelector("#request-rows").replaceChildren(...rows.map((row) => {
    const tr = document.createElement("tr");
    const status = select(REQUEST_STATUSES, row.status);
    status.addEventListener("change", () => patch(`/api/admin/part-requests/${row.id}`, { status: status.value }));
    const td = document.createElement("td"); td.append(status);
    tr.append(
      cell(date(row.created_at)),
      cell(row.query),
      cell(row.contact),
      cell([row.vehicle_label, row.vin].filter(Boolean).join(" · ") || null),
      cell(row.note),
      td,
    );
    return tr;
  }));
}

async function loadFitReports() {
  const response = await fetch("/api/admin/fit-reports");
  if (!response.ok) throw new Error("Fit reports could not be loaded");
  const rows = await response.json();
  document.querySelector("#fit-rows").replaceChildren(...rows.map((row) => {
    const tr = document.createElement("tr");
    tr.append(
      cell(`${row.product_name} (${row.product_id})`),
      cell(row.vehicle_label),
      cell(String(row.fits)),
      cell(String(row.does_not_fit)),
      cell(date(row.last_report)),
    );
    return tr;
  }));
}

Promise.all([loadReservations(), loadPartRequests(), loadFitReports()]).catch((error) => showError(error.message));
