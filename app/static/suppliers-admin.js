const supplierList = document.querySelector("#supplier-admin-list");
const importList = document.querySelector("#supplier-import-list");
const errorBox = document.querySelector("#supplier-admin-error");

function supplierCard(supplier) {
  const node = document.createElement("article"); node.className = "need-item";
  node.innerHTML = `<h3></h3><p class="supplier-stats"></p><form><input name="phone" placeholder="Phone"><input name="telegram" placeholder="Telegram"><input name="address" placeholder="Address"><label><input name="is_active" type="checkbox"> Active</label><button>Save</button></form><form class="import-form"><input name="file" type="file" accept=".xlsx" required><button>Import XLSX</button></form><p class="status"></p>`;
  node.querySelector("h3").textContent = supplier.name;
  node.querySelector(".supplier-stats").textContent = `${supplier.active_offers_count} active offers · Last update: ${supplier.latest_data_update || "never"}`;
  const form = node.querySelector("form");
  form.phone.value = supplier.phone || ""; form.telegram.value = supplier.telegram || ""; form.address.value = supplier.address || ""; form.is_active.checked = supplier.is_active;
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const response = await fetch(`/api/admin/suppliers/${supplier.id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ phone: form.phone.value || null, telegram: form.telegram.value || null, address: form.address.value || null, is_active: form.is_active.checked }) });
    node.querySelector(".status").textContent = response.ok ? "Saved" : "Save failed";
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

Promise.all([loadSuppliers(), loadImports()]).catch((error) => { errorBox.hidden = false; errorBox.textContent = error.message; });
