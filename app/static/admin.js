const metrics = document.querySelector("#metrics");
const errorBox = document.querySelector("#admin-error");
const customDates = document.querySelector("#custom-dates");

const metricDefinitions = [
  ["total_searches", "Total searches", false],
  ["unique_sessions", "Unique sessions", false],
  ["zero_result_rate", "Zero-result rate", true],
  ["successful_search_rate", "Successful search rate", true],
  ["correct_in_top_3_rate", "Correct in top 3", true],
  ["median_search_response_time_ms", "Median response", false, " ms"],
  ["product_click_through_rate", "Product CTR", true],
  ["supplier_click_through_rate", "Supplier CTR", true],
  ["contact_supplier_conversion", "Contact conversion", true],
  ["supplier_offer_views", "Offer views", false],
  ["phone_clicks", "Phone clicks", false],
  ["telegram_clicks", "Telegram clicks", false],
  ["reservation_requests", "Reservations", false],
];

const text = (tag, value, className) => {
  const node = document.createElement(tag);
  node.textContent = value;
  if (className) node.className = className;
  return node;
};

const fixButton = (query) => {
  const button = text("button", "Fix", "fix-button");
  button.type = "button";
  button.addEventListener("click", () => startAlias(query));
  return button;
};

function renderCompact(targetId, rows, value, fixable = false) {
  const target = document.querySelector(targetId);
  target.replaceChildren();
  if (!rows.length) { target.append(text("p", "No data in this period.", "empty-copy")); return; }
  rows.forEach((row) => {
    const item = document.createElement("div"); item.className = "compact-row";
    item.append(text("strong", row.query), text("span", value(row)));
    if (fixable) item.append(fixButton(row.query));
    target.append(item);
  });
}

function render(data) {
  metrics.replaceChildren();
  metricDefinitions.forEach(([key, label, percentage, suffix = ""]) => {
    const card = document.createElement("article"); card.className = "metric";
    card.append(text("span", label, "metric-label"), text("strong", `${data.metrics[key]}${percentage ? "%" : suffix}`, "metric-value"));
    metrics.append(card);
  });

  const needs = document.querySelector("#needs-work"); needs.replaceChildren();
  document.querySelector("#needs-count").textContent = `${data.needs_catalog_work.length} queries`;
  if (!data.needs_catalog_work.length) needs.append(text("p", "No catalog issues detected in this period.", "empty-copy"));
  data.needs_catalog_work.forEach((row) => {
    const item = document.createElement("article"); item.className = "need-item";
    item.append(text("strong", row.query), text("div", row.reasons.join(" · "), "need-reasons"));
    if (row.reasons.includes("Zero results")) item.append(fixButton(row.query));
    needs.append(item);
  });

  renderCompact("#most-searched", data.most_searched_queries, (row) => `${row.search_count} searches`);
  renderCompact("#zero-results", data.top_zero_result_queries, (row) => `${row.search_count} searches`, true);
  renderCompact("#poor-feedback", data.queries_with_poor_feedback, (row) => `${row.success_rate ?? 0}% success`);
  renderCompact("#selected-suppliers", data.most_selected_suppliers.map((row) => ({ query: row.supplier, ...row })), (row) => `${row.selections} selections`);
  renderCompact("#demand-without-supply", data.demand_without_supply, (row) => `${row.search_count} searches · ${row.available_offer_count} offers`);

  const table = document.querySelector("#query-table"); table.replaceChildren();
  data.query_rows.forEach((row) => {
    const tr = document.createElement("tr");
    [row.query, row.search_count, row.result_count, row.success_rate == null ? "—" : `${row.success_rate}%`, row.top3_rate == null ? "—" : `${row.top3_rate}%`, row.clicks, row.contacts, `${row.average_response_time_ms} ms`].forEach((value) => tr.append(text("td", value)));
    table.append(tr);
  });
}

async function load(period = "7d", from = "", to = "") {
  const params = new URLSearchParams({ period });
  if (from) params.set("date_from", from);
  if (to) params.set("date_to", to);
  try {
    const response = await fetch(`/api/admin/search-analytics?${params}`);
    if (!response.ok) throw new Error("Analytics could not be loaded.");
    errorBox.hidden = true;
    render(await response.json());
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  }
}

document.querySelectorAll("[data-period]").forEach((button) => button.addEventListener("click", () => {
  document.querySelectorAll("[data-period]").forEach((item) => item.classList.remove("active"));
  button.classList.add("active");
  const period = button.dataset.period;
  customDates.hidden = period !== "custom";
  if (period !== "custom") load(period);
}));
document.querySelector("#apply-custom").addEventListener("click", () => load("custom", document.querySelector("#date-from").value, document.querySelector("#date-to").value));
load();

const aliasForm = document.querySelector("#alias-form");
const aliasInput = document.querySelector("#alias-input");
const aliasKind = document.querySelector("#alias-kind");
const aliasCanonical = document.querySelector("#alias-canonical");
const aliasStatus = document.querySelector("#alias-status");
let aliasTargets = { product: [], vehicle: [] };
let aliasSourceQuery = null;

function renderTargets() {
  const list = document.querySelector("#alias-targets");
  list.replaceChildren(...aliasTargets[aliasKind.value].map((name) => {
    const node = document.createElement("option"); node.value = name; return node;
  }));
  aliasCanonical.placeholder = aliasKind.value === "product" ? "e.g. shock absorber" : "e.g. Daewoo Nexia";
}

function startAlias(query) {
  aliasSourceQuery = query;
  aliasInput.value = query;
  aliasStatus.textContent = `Fixing “${query}”. Trim it to just the unrecognized word, then pick what it means.`;
  aliasStatus.className = "alias-status";
  document.querySelector("#vocabulary").scrollIntoView({ behavior: "smooth", block: "start" });
  aliasInput.focus();
  aliasInput.select();
}

async function loadAliases() {
  const [aliases, targets] = await Promise.all([
    fetch("/api/admin/search-aliases").then((response) => response.json()),
    fetch("/api/admin/search-aliases/targets").then((response) => response.json()),
  ]);
  aliasTargets = targets;
  renderTargets();
  document.querySelector("#alias-count").textContent = `${aliases.length} ${aliases.length === 1 ? "alias" : "aliases"}`;
  const list = document.querySelector("#alias-list");
  list.replaceChildren();
  if (!aliases.length) list.append(text("p", "No custom aliases yet. Use Fix on a zero-result query to add one.", "empty-copy"));
  aliases.forEach((alias) => {
    const row = document.createElement("div"); row.className = "compact-row alias-row";
    const mapping = document.createElement("strong");
    mapping.append(alias.alias, text("span", " → ", "alias-arrow"), alias.canonical);
    const remove = text("button", "Remove", "fix-button");
    remove.type = "button";
    remove.addEventListener("click", async () => {
      if (remove.dataset.confirm !== "yes") {
        remove.dataset.confirm = "yes"; remove.textContent = "Confirm remove"; return;
      }
      const response = await fetch(`/api/admin/search-aliases/${alias.id}`, { method: "DELETE" });
      if (response.ok) loadAliases();
    });
    row.append(mapping, text("span", alias.kind === "product" ? "Part" : "Car"), remove);
    list.append(row);
  });
}

aliasKind.addEventListener("change", renderTargets);
aliasForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const response = await fetch("/api/admin/search-aliases", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kind: aliasKind.value, alias: aliasInput.value, canonical: aliasCanonical.value, source_query: aliasSourceQuery }),
  });
  const data = await response.json();
  if (!response.ok) {
    aliasStatus.textContent = typeof data.detail === "string" ? data.detail : "Check the alias and target.";
    aliasStatus.className = "alias-status is-error";
    return;
  }
  const found = data.source_query_result_count;
  aliasStatus.textContent = found == null
    ? `Saved: “${data.alias}” → ${data.canonical}.`
    : `Saved: “${data.alias}” → ${data.canonical}. “${aliasSourceQuery}” now finds ${found} ${found === 1 ? "result" : "results"}.`;
  aliasStatus.className = found === 0 ? "alias-status is-error" : "alias-status is-ok";
  aliasForm.reset();
  aliasSourceQuery = null;
  renderTargets();
  loadAliases();
});
loadAliases();
