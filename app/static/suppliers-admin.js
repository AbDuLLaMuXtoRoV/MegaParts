const supplierList = document.querySelector("#supplier-admin-list");
const importList = document.querySelector("#supplier-import-list");
const errorBox = document.querySelector("#supplier-admin-error");

// Shown to buyers as "verified seller"; ticking the box needs the legal name and INN.
const TEXT_FIELDS = [
  ["name", "Name shown to buyers"],
  ["phone", "Phone"],
  ["telegram", "Telegram (@username or link)"],
  ["address", "Address (e.g. Sergeli auto market, row 9)"],
  ["city", "City"],
  ["work_hours", "Hours (e.g. 9:00–18:00, Mon–Sat)"],
  ["map_url", "Map link (https://…)"],
  ["legal_name", "Legal name"],
  ["inn", "INN (9 or 14 digits)"],
  ["licence_number", "Licence number"],
];

function supplierCard(supplier) {
  const node = document.createElement("article"); node.className = "need-item";
  node.innerHTML = `<h3></h3><p class="supplier-stats"></p><p class="supplier-trust"></p><form class="supplier-form"></form><form class="price-list-form"><label>Seller's price list (any layout, .xlsx or .xls) <input name="file" type="file" accept=".xlsx,.xls" required></label><button>Upload price list</button></form><form class="import-form"><label>Strict offer file (supplier_sku column) <input name="file" type="file" accept=".xlsx" required></label><button>Import XLSX</button></form><p class="status"></p><ul class="status-list"></ul>`;
  node.querySelector("h3").textContent = supplier.name;
  node.querySelector(".supplier-stats").textContent = `${supplier.active_offers_count} active offers · Last update: ${supplier.latest_data_update || "never"}`;
  node.querySelector(".supplier-trust").textContent = [
    supplier.verified_at ? `Verified ${supplier.verified_at.slice(0, 10)}` : "Not verified",
    supplier.reliability_score != null
      ? `Reliability ${supplier.reliability_score}% from ${supplier.reliability_sample} finished reservations`
      : `Reliability shown after 5 finished reservations (now ${supplier.reliability_sample})`,
  ].join(" · ");
  const form = node.querySelector(".supplier-form");
  TEXT_FIELDS.forEach(([name, label]) => {
    const input = document.createElement("input");
    input.name = name; input.placeholder = label; input.title = label; input.value = supplier[name] || "";
    form.append(input);
  });
  form.insertAdjacentHTML("beforeend", `<label><input name="is_active" type="checkbox"> Active</label><label><input name="verified" type="checkbox"> Documents checked (verified seller)</label><button>Save</button>`);
  form.is_active.checked = supplier.is_active;
  form.verified.checked = Boolean(supplier.verified_at);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const body = Object.fromEntries(TEXT_FIELDS.map(([name]) => [name, form[name].value.trim() || null]));
    Object.assign(body, { is_active: form.is_active.checked, verified: form.verified.checked });
    const response = await fetch(`/api/admin/suppliers/${supplier.id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const data = await response.json();
    node.querySelector(".status").textContent = response.ok ? "Saved" : (typeof data.detail === "string" ? data.detail : "Save failed: check INN (9 or 14 digits) and map link (https://…)");
    if (response.ok) loadSuppliers();
  });
  node.querySelector(".price-list-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = event.currentTarget.querySelector("button");
    button.disabled = true;
    node.querySelector(".status").textContent = "Reading the list…";
    const response = await fetch(`/api/admin/suppliers/${supplier.id}/price-list`, { method: "POST", body: new FormData(event.currentTarget) });
    const data = await response.json();
    button.disabled = false;
    node.querySelector(".status").textContent = response.ok
      ? `Done: ${data.rows} rows · ${data.parts_created} new parts · ${data.parts_reused} already in the catalog · ${data.offers_created} new offers, ${data.offers_updated} updated, ${data.offers_closed} no longer listed · ${data.rows_without_car} rows without a car${data.cars_created.length ? ` · new cars: ${data.cars_created.join(", ")}` : ""}`
      : (typeof data.detail === "string" ? data.detail : "Upload failed");
    const list = node.querySelector(".status-list");
    list.replaceChildren(...(response.ok ? data.unrecognised : []).map((name) => {
      const item = document.createElement("li"); item.textContent = `Not recognised (kept under the seller's name): ${name}`; return item;
    }));
    if (response.ok) { loadSuppliers(); loadImports(); }
  });
  node.querySelector(".import-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const body = new FormData(event.currentTarget);
    const response = await fetch(`/api/admin/suppliers/${supplier.id}/offers/import`, { method: "POST", body });
    const data = await response.json();
    node.querySelector(".status").textContent = response.ok ? `Imported: ${data.rows_matched} matched, ${data.unmatched_rows} unmatched, ${data.errors} errors` : (data.detail || "Import failed");
    if (response.ok) loadImports();
  });
  return node;
}

async function loadSuppliers() {
  const response = await fetch("/api/admin/suppliers");
  if (!response.ok) throw new Error("Suppliers could not be loaded");
  supplierList.replaceChildren(...(await response.json()).map(supplierCard));
}

async function loadImports() {
  const response = await fetch("/api/admin/supplier-imports");
  if (!response.ok) throw new Error("Imports could not be loaded");
  const imports = await response.json(); importList.replaceChildren();
  imports.forEach((item) => { const row = document.createElement("div"); row.className = "compact-row"; row.textContent = `${item.supplier_name} · ${item.source_filename || "XLSX"} · ${item.status} · ${item.rows_matched} matched / ${item.unmatched_rows} review`; importList.append(row); });
}

document.querySelector("#supplier-create").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const body = Object.fromEntries([...new FormData(form)].map(([key, value]) => [key, String(value).trim() || null]));
  const response = await fetch("/api/admin/suppliers", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await response.json();
  document.querySelector("#supplier-create-status").textContent = response.ok ? `Added ${data.name}. Upload their price list on their card below.` : (typeof data.detail === "string" ? data.detail : "Could not add the seller");
  if (response.ok) { form.reset(); loadSuppliers(); }
});

Promise.all([loadSuppliers(), loadImports()]).catch((error) => { errorBox.hidden = false; errorBox.textContent = error.message; });
