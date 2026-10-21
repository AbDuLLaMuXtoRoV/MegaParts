// IRIZON profile: supplier card, product list, and the full product editor.
const $ = (selector, root = document) => root.querySelector(selector);
const errorBox = $("#catalog-error");
const productForm = $("#product-form");
const productList = $("#product-list");
const PAGE_SIZE = 60;

const state = {
  options: null,
  profile: null,
  record: null,      // product as last loaded/saved
  isNew: false,
  dirty: false,
  listOffset: 0,
};

// Product form field -> workbook "Data Dictionary" key (help text in Uzbek).
const HELP = {
  name: "Products.product_name_uz", name_ru: "Products.product_name_ru", name_en: "Products.product_name_en",
  brand_id: "Products.brand_id", category_id: "Products.category_id", article_number: "Products.article_number",
  origin: "Products.origin", status: "Products.status", unit: "Products.unit", pack_qty: "Products.pack_qty",
  weight_kg: "Products.weight_kg", length_mm: "Products.length_mm", width_mm: "Products.width_mm",
  height_mm: "Products.height_mm", ean: "Products.ean", country_of_origin: "Products.country_of_origin",
  description: "Products.description", universal: "Products.universal",
};

// ---------- small DOM helpers ----------
const el = (tag, props = {}, ...children) => {
  const node = document.createElement(tag);
  Object.entries(props).forEach(([key, value]) => {
    if (value == null || value === false) return;
    if (key === "class") node.className = value;
    else if (key === "dataset") Object.assign(node.dataset, value);
    else if (key in node && key !== "list") node[key] = value;
    else node.setAttribute(key, value === true ? "" : value);
  });
  node.append(...children.flat().filter((child) => child != null && child !== false));
  return node;
};
const option = (value, label, selected) => el("option", { value, selected: String(value) === String(selected ?? "") }, label);
const listOptions = (name) => state.options.lists[name] || [];
const showError = (message) => { errorBox.textContent = message; errorBox.hidden = !message; };

async function api(url, init = {}) {
  const response = await fetch(url, {
    ...init,
    headers: init.body ? { "Content-Type": "application/json" } : undefined,
  });
  const data = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    const error = new Error(typeof data?.detail === "string" ? data.detail : `Request failed (${response.status})`);
    error.status = response.status;
    // Our validator sends {errors: [{field, message}]}; FastAPI's schema check sends [{loc, msg}].
    error.details = Array.isArray(data?.detail)
      ? data.detail.map((item) => ({ field: item.loc.slice(1).join("."), message: item.msg.replace(/^String should have at least 1 character$/, "Required") }))
      : data?.detail?.errors || [];
    throw error;
  }
  return data;
}

// ---------- profile card ----------
const PROFILE_FIELDS = [
  ["name", "Company name", "text"],
  ["supplier_type", "Type", "list:supplier_type"],
  ["city", "City", "text"],
  ["address", "Address", "text"],
  ["phone", "Phone", "tel"],
  ["telegram", "Telegram", "text"],
  ["contact", "Contact person / notes", "text"],
  ["default_currency", "Default currency", "list:currency"],
  ["integration", "Price-list integration", "list:integration"],
  ["update_frequency_days", "Updates every (days)", "number"],
  ["default_lead_time_days", "Default lead time (days)", "number"],
  ["is_active", "Active supplier", "checkbox"],
];

function renderProfile() {
  const { profile } = state;
  const supplier = profile.suppliers[0];
  $("#user-chip").textContent = profile.username;
  $("#profile-name").textContent = supplier?.name || "IRIZON";
  $("#profile-avatar").textContent = (supplier?.name || "I").trim()[0].toUpperCase();
  $("#profile-meta").textContent = supplier
    ? [supplier.supplier_type, supplier.city, supplier.phone, supplier.telegram, supplier.default_currency].filter(Boolean).join(" · ")
    : "";

  const stats = $("#profile-stats");
  stats.replaceChildren();
  const s = profile.stats;
  [
    ["Products", s.products, ""],
    ["Live in search", s.searchable, ""],
    ["Hidden (conflict)", s.hidden_conflicts, "conflict"],
    ["Open review items", s.open_reviews, "review"],
    ["Offers without price", s.offers_without_price, "no_price"],
    ["Categories", s.categories, null],
    ["Vehicles", s.vehicles, null],
  ].forEach(([label, value, issue]) => {
    const content = [el("strong", {}, String(value)), el("span", {}, label)];
    stats.append(issue === null
      ? el("div", { class: "stat" }, content)
      : el("button", { type: "button", class: "stat stat-link", onclick: () => { $("#filter-issue").value = issue; loadProducts(); } }, content));
  });

  const form = $("#profile-form");
  form.replaceChildren();
  if (!supplier) return;
  const grid = el("div", { class: "field-grid" });
  PROFILE_FIELDS.forEach(([key, label, type]) => grid.append(field({ key, label, type, value: supplier[key], scope: "profile" })));
  form.append(grid, el("div", { class: "form-actions" },
    el("p", { class: "form-status", id: "profile-status", role: "status" }),
    el("button", { type: "button", class: "secondary-button", onclick: toggleProfileForm }, "Cancel"),
    el("button", { type: "submit", class: "primary-button" }, "Save profile")));
}

function toggleProfileForm() {
  const form = $("#profile-form");
  form.hidden = !form.hidden;
  $("#edit-profile").setAttribute("aria-expanded", String(!form.hidden));
  if (!form.hidden) form.querySelector("input")?.focus();
}

$("#edit-profile").addEventListener("click", toggleProfileForm);
$("#profile-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const supplier = state.profile.suppliers[0];
  const payload = {};
  PROFILE_FIELDS.forEach(([key, , type]) => { payload[key] = readInput(form.querySelector(`[data-field="${key}"]`), type); });
  clearFieldErrors(form);
  try {
    await api(`/api/admin/catalog/suppliers/${supplier.id}`, { method: "PUT", body: JSON.stringify(payload) });
    state.profile = await api("/api/admin/catalog/profile");
    renderProfile();
    $("#profile-form").hidden = false;
    $("#profile-status").textContent = "Profile saved.";
  } catch (error) {
    showFieldErrors(form, error.details);
    $("#profile-status").textContent = error.details.length ? "Fix the highlighted fields." : error.message;
  }
});

// ---------- generic field rendering ----------
function field({ key, label, type = "text", value, required = false, help, scope, hint, wide = false }) {
  const id = `${scope || "f"}-${key}`.replace(/[^\w-]/g, "_");
  let input;
  if (type === "checkbox") {
    input = el("input", { type: "checkbox", id, checked: Boolean(value) });
  } else if (type.startsWith("list:") || type === "select") {
    const values = type.startsWith("list:") ? listOptions(type.slice(5)).map((item) => [item, item]) : [];
    input = el("select", { id }, option("", required ? "Choose…" : "—"), values.map(([v, l]) => option(v, l, value)));
  } else if (type === "textarea") {
    input = el("textarea", { id, rows: 3 }, value ?? "");
  } else {
    input = el("input", { id, type: type === "decimal" ? "text" : type, value: value ?? "", inputmode: type === "decimal" ? "decimal" : undefined, step: type === "number" ? "1" : undefined, min: type === "number" ? "0" : undefined });
  }
  input.dataset.field = key;
  input.dataset.type = type;
  if (required) input.required = true;
  const helpText = help || (state.options.help[HELP[key]] ?? "");
  const wrapper = el("div", { class: `field${type === "checkbox" ? " field-check" : ""}${wide ? " field-wide" : ""}` });
  const labelNode = el("label", { for: id }, label, required ? el("span", { class: "required", title: "Required" }, " *") : null);
  if (type === "checkbox") wrapper.append(input, labelNode); else wrapper.append(labelNode, input);
  if (hint) wrapper.append(el("small", { class: "hint" }, hint));
  else if (helpText) wrapper.append(el("small", { class: "hint", title: helpText }, helpText));
  wrapper.append(el("small", { class: "field-error", "aria-live": "polite" }));
  return wrapper;
}

function readInput(input, type = input.dataset.type) {
  if (!input) return null;
  if (type === "checkbox") return input.checked;
  const value = input.value.trim();
  if (value === "") return null;
  if (type === "number") return Number.parseInt(value, 10);
  if (type === "id") return Number.parseInt(value, 10);
  if (type === "decimal") return value.replace(",", ".");
  return value;
}

function clearFieldErrors(root) {
  root.querySelectorAll(".has-error").forEach((node) => node.classList.remove("has-error"));
  root.querySelectorAll(".field-error").forEach((node) => { node.textContent = ""; });
}

function showFieldErrors(root, errors) {
  let first = null;
  errors.forEach(({ field: path, message }) => {
    const [section, index, key] = path.split(".");
    const input = key
      ? root.querySelector(`[data-row="${section}"][data-index="${index}"] [data-field="${key}"]`)
      : root.querySelector(`[data-field="${section}"]`);
    const holder = input?.closest(".field, .row-cell");
    if (!holder) return;
    holder.classList.add("has-error");
    holder.querySelector(".field-error").textContent = message;
    first = first || input;
  });
  first?.focus();
}

// ---------- product list ----------
let searchTimer = null;
async function loadProducts(append = false) {
  if (!append) state.listOffset = 0;
  const params = new URLSearchParams({ limit: String(PAGE_SIZE), offset: String(state.listOffset) });
  const q = $("#product-search").value.trim();
  if (q) params.set("q", q);
  if ($("#filter-category").value) params.set("category_id", $("#filter-category").value);
  if ($("#filter-brand").value) params.set("brand_id", $("#filter-brand").value);
  if ($("#filter-issue").value) params.set("issue", $("#filter-issue").value);
  try {
    const data = await api(`/api/admin/catalog/products?${params}`);
    if (!append) productList.replaceChildren();
    data.items.forEach((item) => productList.append(productListItem(item)));
    state.listOffset += data.items.length;
    $("#list-count").textContent = `${data.total} ${data.total === 1 ? "product" : "products"}`;
    $("#load-more").hidden = state.listOffset >= data.total;
    markActive();
  } catch (error) {
    showError(error.message);
  }
}

function productListItem(item) {
  const badges = [];
  if (!item.is_searchable) badges.push(el("span", { class: "badge badge-danger" }, item.audit_status === "CONFLICT" ? "Hidden" : "Off"));
  else if (["REVIEW", "PROBABLE"].includes(item.audit_status)) badges.push(el("span", { class: "badge badge-warn" }, item.audit_status.toLowerCase()));
  return el("li", {},
    el("button", { type: "button", class: "product-item", dataset: { id: item.id }, onclick: () => openProduct(item.id) },
      el("span", { class: "product-item-top" }, el("span", { class: "product-id" }, item.id), badges),
      el("span", { class: "product-item-name" }, item.name),
      el("span", { class: "product-item-meta" }, [item.brand || "No brand", item.article_number, item.category].filter(Boolean).join(" · "))));
}

function markActive() {
  productList.querySelectorAll(".product-item").forEach((node) => {
    const active = node.dataset.id === state.record?.id;
    node.classList.toggle("is-active", active);
    if (active) node.setAttribute("aria-current", "true"); else node.removeAttribute("aria-current");
  });
}

$("#product-search").addEventListener("input", () => { clearTimeout(searchTimer); searchTimer = setTimeout(() => loadProducts(), 250); });
["#filter-category", "#filter-brand", "#filter-issue"].forEach((selector) => $(selector).addEventListener("change", () => loadProducts()));
$("#load-more").addEventListener("click", () => loadProducts(true));

// ---------- product editor ----------
const confirmDiscard = () => !state.dirty || window.confirm("You have unsaved changes. Discard them?");

async function openProduct(id) {
  if (state.record?.id === id && !state.isNew) return;
  if (!confirmDiscard()) return;
  try {
    const record = await api(`/api/admin/catalog/products/${encodeURIComponent(id)}`);
    renderEditor(record, false);
    history.replaceState(null, "", `/admin/catalog?product=${encodeURIComponent(id)}`);
  } catch (error) {
    showError(error.message);
  }
}

$("#new-product").addEventListener("click", () => {
  if (!confirmDiscard()) return;
  const supplier = state.profile.suppliers[0];
  renderEditor({
    id: null, name: "", name_ru: null, name_en: null, brand_id: null, category_id: "", article_number: null,
    origin: "AFTERMARKET", status: "ACTIVE", unit: "PCS", universal: false,
    attributes: [], references: [], fitments: [], audits: [], review_items: [], missing_required_attributes: [],
    offers: supplier ? [{ id: null, supplier_id: supplier.id, currency: supplier.default_currency || "UZS", is_active: true, data_status: "LIVE" }] : [],
  }, true);
  history.replaceState(null, "", "/admin/catalog");
});

function section(title, ...content) {
  return el("fieldset", { class: "form-section" }, el("legend", {}, title), content);
}

function renderEditor(record, isNew) {
  state.record = record;
  state.isNew = isNew;
  state.dirty = false;
  showError("");
  $("#editor-empty").hidden = true;
  productForm.hidden = false;
  productForm.replaceChildren();
  const { options } = state;

  const status = isNew
    ? el("span", { class: "badge" }, "New product")
    : record.is_searchable
      ? el("span", { class: "badge badge-ok" }, "Live in search")
      : el("span", { class: "badge badge-danger" }, record.audit_status === "CONFLICT" ? "Hidden — merge conflict" : `Hidden — status ${record.status}`);
  productForm.append(el("header", { class: "editor-header" },
    el("div", {}, el("p", { class: "eyebrow" }, isNew ? "Create" : record.id), el("h2", {}, isNew ? "New product" : record.name)),
    status));

  const categoryOptions = options.categories.map((category) => option(category.id, `${category.parent_id ? "— " : ""}${category.name_uz} (${category.id})`, record.category_id));
  const brandSelect = field({ key: "brand_id", label: "Brand", type: "select", value: record.brand_id, hint: "Recommended — leave empty only for unbranded parts" });
  $("select", brandSelect).append(...options.brands.map((brand) => option(brand.id, brand.name, record.brand_id)));
  $("select", brandSelect).dataset.type = "id";
  const categorySelect = field({ key: "category_id", label: "Category", type: "select", value: record.category_id, required: true });
  $("select", categorySelect).append(...categoryOptions);
  $("select", categorySelect).addEventListener("change", () => renderAttributes(collectAttributes()));

  productForm.append(section("Basics", el("div", { class: "field-grid" },
    field({ key: "name", label: "Name (Uzbek)", value: record.name, required: true, wide: true }),
    field({ key: "name_ru", label: "Name (Russian)", value: record.name_ru }),
    field({ key: "name_en", label: "Name (English)", value: record.name_en }),
    brandSelect,
    field({ key: "article_number", label: "Article number", value: record.article_number, hint: "Recommended — the brand's own part code" }),
    categorySelect,
    field({ key: "origin", label: "Origin", type: "list:origin", value: record.origin, required: true }),
    field({ key: "status", label: "Status", type: "list:product_status", value: record.status, required: true, hint: "Only ACTIVE products appear in search" }),
    field({ key: "unit", label: "Unit", type: "list:unit", value: record.unit, required: true }),
    field({ key: "universal", label: "Universal part (fits any vehicle)", type: "checkbox", value: record.universal }))));

  productForm.append(section("Specifications", el("div", { class: "field-grid" },
    field({ key: "pack_qty", label: "Pack quantity", type: "number", value: record.pack_qty }),
    field({ key: "weight_kg", label: "Weight (kg)", type: "decimal", value: record.weight_kg }),
    field({ key: "length_mm", label: "Length (mm)", type: "decimal", value: record.length_mm }),
    field({ key: "width_mm", label: "Width (mm)", type: "decimal", value: record.width_mm }),
    field({ key: "height_mm", label: "Height (mm)", type: "decimal", value: record.height_mm }),
    field({ key: "ean", label: "EAN barcode", value: record.ean }),
    field({ key: "country_of_origin", label: "Country of origin", value: record.country_of_origin }),
    field({ key: "description", label: "Description", type: "textarea", value: record.description, wide: true }))));

  productForm.append(el("fieldset", { class: "form-section", id: "attributes-section" }));
  renderAttributes(record.attributes);

  productForm.append(repeatSection("references", "Reference numbers", record.references, referenceRow, () => ({ type: "AFTERMARKET" }), "+ Add reference"));
  productForm.append(repeatSection("fitments", "Fits vehicles", record.fitments, fitmentRow, () => ({}), "+ Add vehicle"));
  productForm.append(repeatSection("offers", "Supplier offers (price & stock)", record.offers, offerRow, () => {
    const supplier = state.profile.suppliers[0];
    return { supplier_id: supplier?.id, currency: supplier?.default_currency || "UZS", is_active: true, data_status: "LIVE" };
  }, "+ Add offer", "Removing an offer deactivates it, so existing reservations keep working."));

  if (!isNew && (record.audits.length || record.review_items.length)) {
    productForm.append(section("Audit & review (from the workbook)",
      el("ul", { class: "audit-list" },
        record.audits.map((audit) => el("li", {}, el("span", { class: `badge ${audit.merge_status === "CONFLICT" ? "badge-danger" : "badge-warn"}` }, audit.merge_status), " ", audit.audit_reason || "")),
        record.review_items.map((item) => el("li", {}, el("span", { class: "badge" }, item.status), " ", `${item.raw_id}: ${item.review_reason}`)))));
  }
  if (!isNew && record.source_rows) {
    productForm.append(el("p", { class: "source-note" }, `Source rows: ${record.source_rows} · merge basis: ${record.merge_basis || "—"}`));
  }

  productForm.append(el("div", { class: "save-bar" },
    el("p", { class: "form-status", id: "save-status", role: "status" }, isNew ? "Fill in the required fields (*) and save." : "No changes."),
    el("button", { type: "button", class: "secondary-button", id: "discard-changes", disabled: !isNew, onclick: discardChanges }, "Discard"),
    el("button", { type: "submit", class: "primary-button", id: "save-product" }, isNew ? "Create product" : "Save changes")));
  markActive();
}

function discardChanges() {
  if (state.isNew) {
    state.dirty = false;
    state.record = null;
    productForm.hidden = true;
    $("#editor-empty").hidden = false;
    return;
  }
  state.dirty = false;
  renderEditor(state.record, false);
}

productForm.addEventListener("input", () => {
  if (state.dirty) return;
  state.dirty = true;
  $("#save-status").textContent = "Unsaved changes";
  $("#discard-changes").disabled = false;
});
window.addEventListener("beforeunload", (event) => { if (state.dirty) event.preventDefault(); });

// ----- attributes (driven by the category's attribute definitions) -----
function collectAttributes() {
  return [...productForm.querySelectorAll("[data-attribute]")].map((input) => ({
    attribute_code: input.dataset.attribute,
    value: input.value,
    unit: input.dataset.unit || null,
  }));
}

function renderAttributes(current) {
  const holder = $("#attributes-section");
  const categoryId = productForm.querySelector('[data-field="category_id"]')?.value;
  const category = state.options.categories.find((item) => item.id === categoryId);
  const definitions = category?.attributes || [];
  const values = Object.fromEntries(current.map((item) => [item.attribute_code, item]));
  holder.replaceChildren(el("legend", {}, "Attributes"));
  const grid = el("div", { class: "field-grid" });
  definitions.forEach((definition) => {
    const id = `attr-${definition.attribute_code}`;
    const value = values[definition.attribute_code]?.value ?? "";
    let input;
    if (definition.data_type === "ENUM" && definition.allowed_values.length) {
      input = el("select", { id }, option("", "—"), definition.allowed_values.map((item) => option(item, item, value)));
    } else if (definition.data_type === "BOOL") {
      input = el("select", { id }, option("", "—"), option("Y", "Yes", value), option("N", "No", value));
    } else {
      input = el("input", { id, value, inputmode: definition.data_type === "NUMBER" ? "decimal" : undefined });
    }
    input.dataset.attribute = definition.attribute_code;
    input.dataset.unit = definition.unit || "";
    input.dataset.field = definition.attribute_code;
    const label = `${definition.name_uz}${definition.unit ? ` (${definition.unit})` : ""}`;
    grid.append(el("div", { class: "field" },
      el("label", { for: id }, label, definition.required ? el("span", { class: "required-soft", title: "Required by the category" }, " •") : null),
      input,
      el("small", { class: "hint" }, definition.name_ru || definition.attribute_code),
      el("small", { class: "field-error" })));
  });
  // Values that the category does not define stay editable instead of being dropped.
  const known = new Set(definitions.map((definition) => definition.attribute_code));
  current.filter((item) => !known.has(item.attribute_code) && item.value).forEach((item) => {
    const id = `attr-${item.attribute_code}`;
    const input = el("input", { id, value: item.value });
    input.dataset.attribute = item.attribute_code;
    input.dataset.unit = item.unit || "";
    grid.append(el("div", { class: "field" }, el("label", { for: id }, item.attribute_code), input, el("small", { class: "hint" }, "Not defined for this category"), el("small", { class: "field-error" })));
  });
  if (!grid.children.length) grid.append(el("p", { class: "empty-copy" }, category ? "This category has no attribute definitions." : "Choose a category to see its attributes."));
  holder.append(grid);
  const missing = definitions.filter((definition) => definition.required && !values[definition.attribute_code]?.value);
  if (missing.length) holder.append(el("p", { class: "soft-warning" }, `Recommended for this category: ${missing.map((item) => item.name_uz).join(", ")}.`));
}

// ----- repeating rows (references, fitments, offers) -----
function repeatSection(name, title, rows, rowBuilder, blank, addLabel, note) {
  const body = el("div", { class: "rows", dataset: { rows: name } });
  const renumber = () => body.querySelectorAll(":scope > [data-row]").forEach((row, index) => { row.dataset.index = String(index); });
  const addRow = (data) => {
    const row = rowBuilder(data);
    row.dataset.row = name;
    row.dataset.id = data.id ?? "";
    row.append(el("div", { class: "row-cell row-remove" },
      el("button", { type: "button", class: "remove-row", "aria-label": `Remove ${title.toLowerCase()} row`, onclick: () => { row.remove(); renumber(); markDirty(); } }, "✕")));
    body.append(row);
    renumber();
    return row;
  };
  rows.forEach(addRow);
  return section(title,
    note ? el("p", { class: "hint section-note" }, note) : null,
    body,
    el("button", { type: "button", class: "add-row", onclick: () => { const row = addRow(blank()); markDirty(); row.querySelector("input, select")?.focus(); } }, addLabel));
}

function markDirty() { productForm.dispatchEvent(new Event("input")); }

function cell(label, input, className = "") {
  return el("div", { class: `row-cell ${className}` }, el("span", { class: "cell-label" }, label), input, el("small", { class: "field-error" }));
}
function cellInput(key, value, props = {}) {
  const type = props.type || "text";
  const input = el("input", { value: value ?? "", ...props, type: type === "decimal" ? "text" : type, inputmode: type === "decimal" ? "decimal" : props.inputmode });
  input.dataset.field = key;
  input.dataset.type = type;
  input.setAttribute("aria-label", props["aria-label"] || key);
  return input;
}
function cellSelect(key, values, value, { blank = "—", type = "text" } = {}) {
  const input = el("select", {}, option("", blank), values.map(([v, l]) => option(v, l, value)));
  input.dataset.field = key;
  input.dataset.type = type;
  return input;
}
function cellCheck(key, value) {
  const input = el("input", { type: "checkbox", checked: Boolean(value) });
  input.dataset.field = key;
  input.dataset.type = "checkbox";
  return input;
}
const pairs = (values) => values.map((value) => [value, value]);

function referenceRow(data) {
  return el("div", { class: "row row-reference" },
    cell("Number", cellInput("number", data.number, { required: true, "aria-label": "Reference number" }), "cell-wide"),
    cell("Type", cellSelect("type", pairs(listOptions("ref_type")), data.type, { blank: "Choose…" })),
    cell("Number brand", cellSelect("number_brand_id", state.options.brands.map((brand) => [brand.id, brand.name]), data.number_brand_id, { type: "id" })),
    cell("Confidence", cellSelect("confidence", pairs(listOptions("confidence")), data.confidence)),
    cell("Verified", cellCheck("verified", data.verified), "cell-narrow"),
    cell("Notes", cellInput("notes", data.notes), "cell-wide"));
}

function fitmentRow(data) {
  return el("div", { class: "row row-fitment" },
    cell("Vehicle", cellSelect("vehicle_id", state.options.vehicles.map((vehicle) => [vehicle.id, vehicle.label]), data.vehicle_id, { blank: "Choose vehicle…" }), "cell-vehicle"),
    cell("Position", cellSelect("position", pairs(listOptions("position")), data.position)),
    cell("Side", cellSelect("side", pairs(listOptions("side")), data.side)),
    cell("Qty / car", cellInput("qty_per_vehicle", data.qty_per_vehicle, { type: "number", min: "0" }), "cell-narrow"),
    cell("Year from", cellInput("year_from", data.year_from, { type: "number", min: "1900", max: "2100" }), "cell-narrow"),
    cell("Year to", cellInput("year_to", data.year_to, { type: "number", min: "1900", max: "2100" }), "cell-narrow"),
    cell("Source", cellSelect("fitment_source", pairs(listOptions("fitment_source")), data.fitment_source)),
    cell("Confidence", cellSelect("confidence", pairs(listOptions("confidence")), data.confidence)),
    cell("Verified", cellCheck("verified", data.verified), "cell-narrow"),
    cell("Note", cellInput("condition_note", data.condition_note), "cell-wide"));
}

function offerRow(data) {
  const pill = el("span", { class: `badge ${data.data_status === "LIVE" ? "badge-ok" : "badge-warn"}`, title: data.data_status === "LIVE" ? "Live data" : "Imported demo data — editing the price or stock makes it live" }, data.data_status || "LIVE");
  return el("div", { class: "row row-offer" },
    cell("Supplier", cellSelect("supplier_id", state.options.suppliers.map((supplier) => [supplier.id, supplier.name]), data.supplier_id, { blank: "Choose…", type: "id" }), "cell-wide"),
    cell("Supplier SKU", cellInput("supplier_sku", data.supplier_sku)),
    cell("Price", cellInput("price", data.price, { type: "decimal", placeholder: "on request" })),
    cell("Currency", cellSelect("currency", pairs(listOptions("currency")), data.currency || "UZS", { blank: "UZS" }), "cell-narrow"),
    cell("Stock", cellInput("stock_qty", data.stock_qty, { type: "number", min: "0", placeholder: "?" }), "cell-narrow"),
    cell("Warehouse", cellInput("warehouse", data.warehouse)),
    cell("Lead days", cellInput("lead_time_days", data.lead_time_days, { type: "number", min: "0" }), "cell-narrow"),
    cell("Min order", cellInput("min_order_qty", data.min_order_qty, { type: "number", min: "0" }), "cell-narrow"),
    cell("Condition", cellSelect("condition", pairs(listOptions("condition")), data.condition)),
    cell("Price type", cellSelect("price_type", pairs(listOptions("price_type")), data.price_type)),
    cell("Active", cellCheck("is_active", data.is_active ?? true), "cell-narrow"),
    cell("Data", pill, "cell-narrow"));
}

function collectRows(name) {
  return [...productForm.querySelectorAll(`[data-row="${name}"]`)].map((row) => {
    const item = row.dataset.id ? { id: Number(row.dataset.id) } : {};
    row.querySelectorAll("[data-field]").forEach((input) => { item[input.dataset.field] = readInput(input); });
    return item;
  });
}

function collectPayload() {
  const payload = {};
  productForm.querySelectorAll("[data-field]:not([data-attribute])").forEach((input) => {
    if (input.closest("[data-row]")) return;
    payload[input.dataset.field] = readInput(input);
  });
  payload.name = payload.name || "";
  payload.category_id = payload.category_id || "";
  payload.attributes = collectAttributes();
  payload.references = collectRows("references");
  payload.fitments = collectRows("fitments");
  payload.offers = collectRows("offers").map((offer) => ({ ...offer, currency: offer.currency || "UZS", is_active: offer.is_active ?? true }));
  if (!state.isNew) payload.expected_updated_at = state.record.updated_at;
  return payload;
}

productForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearFieldErrors(productForm);
  const status = $("#save-status");
  const button = $("#save-product");
  button.disabled = true;
  status.textContent = "Saving…";
  try {
    const url = state.isNew ? "/api/admin/catalog/products" : `/api/admin/catalog/products/${encodeURIComponent(state.record.id)}`;
    const saved = await api(url, { method: state.isNew ? "POST" : "PUT", body: JSON.stringify(collectPayload()) });
    const created = state.isNew;
    renderEditor(saved, false);
    $("#save-status").textContent = created ? `Created ${saved.id}.` : "Saved — search is updated.";
    history.replaceState(null, "", `/admin/catalog?product=${encodeURIComponent(saved.id)}`);
    state.profile = await api("/api/admin/catalog/profile");
    renderProfile();
    loadProducts();
  } catch (error) {
    button.disabled = false;
    if (error.status === 422 && error.details.length) {
      showFieldErrors(productForm, error.details);
      status.textContent = `${error.details.length} ${error.details.length === 1 ? "field needs" : "fields need"} attention.`;
    } else if (error.status === 422) {
      status.textContent = "Fill in the required fields (*).";
    } else {
      status.textContent = error.message;
    }
  }
});

// ---------- start ----------
(async () => {
  try {
    [state.options, state.profile] = await Promise.all([api("/api/admin/catalog/options"), api("/api/admin/catalog/profile")]);
  } catch (error) {
    showError(error.message);
    return;
  }
  renderProfile();
  $("#filter-category").append(...state.options.categories.map((category) => option(category.id, `${category.parent_id ? "— " : ""}${category.name_uz}`)));
  $("#filter-brand").append(...state.options.brands.map((brand) => option(brand.id, brand.name)));
  await loadProducts();
  const initial = new URLSearchParams(location.search).get("product");
  if (initial) openProduct(initial);
})();
