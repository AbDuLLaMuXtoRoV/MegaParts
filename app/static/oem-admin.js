const errorBox = document.querySelector("#oem-error");
const filters = document.querySelector("#missing-filters");
const missingRows = document.querySelector("#missing-rows");
const moreButton = document.querySelector("#missing-more");
const uploadStatus = document.querySelector("#upload-status");
const PAGE = 50;
let offset = 0;

function el(tag, attributes = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attributes).forEach(([key, value]) => {
    if (value === undefined || value === null || value === false) return;
    if (key === "text") node.textContent = value;
    else if (key === "onclick") node.addEventListener("click", value);
    else node.setAttribute(key, value);
  });
  node.append(...[].concat(children).filter((child) => child !== null && child !== undefined && child !== false));
  return node;
}

const date = (value) => (value ? new Date(value).toLocaleString("en-GB", { dateStyle: "short", timeStyle: "short" }) : "—");
const count = (value) => Number(value).toLocaleString("en-US");
const partLink = (id, name) => el("a", { href: `/part/${encodeURIComponent(id)}`, target: "_blank", rel: "noopener", text: name });

function showError(message) {
  errorBox.hidden = false;
  errorBox.textContent = message;
}

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "The request failed. Reload the page and try again.");
  return data;
}

const sendJson = (url, method, body) => request(url, { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

function filterParams() {
  const params = new URLSearchParams();
  const data = new FormData(filters);
  ["supplier_id", "q"].forEach((key) => { if (data.get(key)) params.set(key, data.get(key)); });
  return params;
}

async function loadSummary() {
  const summary = await request("/api/admin/oem/summary");
  const share = summary.total ? Math.round((summary.with_oem / summary.total) * 100) : 0;
  document.querySelector("#metric-with").textContent = `${count(summary.with_oem)} of ${count(summary.total)} · ${share}%`;
  document.querySelector("#metric-missing").textContent = count(summary.total - summary.with_oem);
  const select = filters.elements.supplier_id;
  if (select.options.length === 1) {
    summary.sellers.forEach((seller) => select.append(el("option", { value: seller.id, text: seller.name })));
  }
  document.querySelector("#seller-rows").replaceChildren(...summary.sellers.map((seller) => el("tr", {}, [
    el("td", { text: seller.name }),
    el("td", { text: count(seller.parts) }),
    el("td", { text: `${count(seller.with_oem)} (${seller.parts ? Math.round((seller.with_oem / seller.parts) * 100) : 0}%)` }),
    el("td", { text: count(seller.parts - seller.with_oem) }),
    el("td", {}, seller.parts > seller.with_oem ? el("button", {
      type: "button",
      class: "fix-button",
      text: "Show missing",
      onclick: () => {
        select.value = String(seller.id);
        filters.elements.q.value = "";
        loadMissing(true);
        filters.scrollIntoView({ behavior: "smooth" });
      },
    }) : null),
  ])));
}

async function loadSuggestions() {
  const rows = await request("/api/admin/oem/suggestions");
  document.querySelector("#metric-sent").textContent = count(rows.length);
  document.querySelector("#suggestion-count").textContent = rows.length ? `${rows.length} to check` : "";
  document.querySelector("#suggestion-rows").replaceChildren(...(rows.length ? rows.map((row) => {
    const actions = el("td");
    const decide = async (status) => {
      try {
        await sendJson(`/api/admin/oem/suggestions/${row.id}`, "PATCH", { status });
        actions.replaceChildren(el("span", { class: "oem-done", text: status === "ACCEPTED" ? "✓ Added to the part" : "Rejected" }));
        loadSummary();
      } catch (error) { showError(error.message); }
    };
    actions.append(
      el("button", { type: "button", class: "fix-button", text: "Accept", onclick: () => decide("ACCEPTED") }), " ",
      el("button", { type: "button", class: "fix-button", text: "Reject", onclick: () => decide("REJECTED") }),
    );
    return el("tr", {}, [
      el("td", { text: date(row.created_at) }),
      el("td", {}, [partLink(row.product_id, row.product_name), el("div", { class: "oem-sub", text: row.product_id })]),
      el("td", { class: "mono", text: row.number }),
      el("td", { class: "mono", text: row.oem.map((item) => item.number).join(", ") || "—" }),
      actions,
    ]);
  }) : [el("tr", {}, el("td", { colspan: "5", class: "oem-sub", text: "No codes waiting." }))]));
}

// The saved codes of a part, each one typed in by staff with a Remove button for typos.
function savedCodes(row, oem, alsoOn = []) {
  const holder = el("div", { class: "oem-saved" });
  oem.forEach((item) => {
    holder.append(el("span", { class: "oem-chip is-saved" }, [
      `✓ ${item.number}`,
      item.manual ? el("button", {
        type: "button",
        class: "oem-chip-remove",
        "aria-label": `Remove ${item.number}`,
        text: "×",
        onclick: async () => {
          try {
            const result = await request(`/api/admin/oem/parts/${encodeURIComponent(row.id)}/${encodeURIComponent(item.number)}`, { method: "DELETE" });
            holder.replaceWith(result.oem.length ? savedCodes(row, result.oem) : codeForm(row));
            loadSummary();
          } catch (error) { showError(error.message); }
        },
      }) : null,
    ]));
  });
  if (alsoOn.length) {
    holder.append(el("p", { class: "oem-sub" }, ["Same code is also on: ", ...alsoOn.flatMap((part, index) => [index ? ", " : "", partLink(part.id, `${part.name} (${part.id})`)])]));
  }
  return holder;
}

function codeForm(row) {
  const input = el("input", { class: "oem-input", "aria-label": `OEM code for ${row.name}`, placeholder: "e.g. 96273708", maxlength: "200" });
  const status = el("p", { class: "oem-sub", role: "status" });
  const form = el("form", { class: "oem-form" }, [input, el("button", { class: "fix-button", text: "Save" }), status]);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const numbers = input.value.split(/[,;\n]+/).map((value) => value.trim()).filter(Boolean);
    if (!numbers.length) { input.focus(); return; }
    try {
      const result = await sendJson(`/api/admin/oem/parts/${encodeURIComponent(row.id)}`, "POST", { numbers });
      form.replaceWith(savedCodes(row, result.oem, result.also_on));
      loadSummary();
    } catch (error) {
      status.textContent = error.message;
      status.classList.add("is-error");
    }
  });
  row.fill = (number) => {
    const current = input.value.split(/[,;]+/).map((value) => value.trim()).filter(Boolean);
    if (!current.includes(number)) input.value = [...current, number].join(", ");
    input.focus();
  };
  return form;
}

function hintChips(row) {
  const chips = [
    ...row.suggestions.map((item) => el("button", {
      type: "button", class: "oem-chip is-sent", title: `Sent by a buyer on ${date(item.created_at)}`, text: `Buyer: ${item.number}`, onclick: () => row.fill(item.number),
    })),
    ...row.candidates.map((item) => el("button", {
      type: "button", class: "oem-chip", title: `From "${item.name}" (${item.brand || "no brand"}, ${item.product_id}). Check before saving.`, text: item.number, onclick: () => row.fill(item.number),
    })),
  ];
  const lookup = el("a", {
    class: "oem-sub",
    href: `https://www.google.com/search?q=${encodeURIComponent(`${row.seller_names[0] || row.name} ${row.cars[0] || ""} OEM`)}`,
    target: "_blank",
    rel: "noopener",
    text: "Search online ↗",
  });
  return el("div", { class: "oem-hints" }, [...chips, lookup]);
}

function missingRow(row) {
  const formCell = el("td", {}, codeForm(row));
  return el("tr", {}, [
    el("td", {}, [
      partLink(row.id, row.name),
      el("div", { class: "oem-sub", text: [row.id, row.category, row.brand].filter(Boolean).join(" · ") }),
      el("div", { class: "oem-sub", text: row.sellers.join(", ") }),
    ]),
    el("td", { class: "oem-sub", text: row.seller_names.join(" | ") || "—" }),
    el("td", { text: row.cars.join(", ") || "—" }),
    el("td", { class: "mono", text: row.numbers.map((item) => `${item.number} (${item.type.toLowerCase().replace("_", " ")})`).join(", ") || "—" }),
    el("td", {}, hintChips(row)),
    formCell,
  ]);
}

async function loadMissing(fresh = false) {
  if (fresh) offset = 0;
  const params = filterParams();
  document.querySelector("#excel-download").href = `/api/admin/oem/missing.xlsx${params.toString() ? `?${params}` : ""}`;
  params.set("offset", String(offset));
  params.set("limit", String(PAGE));
  const data = await request(`/api/admin/oem/missing?${params}`);
  const rows = data.items.map(missingRow);
  if (fresh) missingRows.replaceChildren(...rows); else missingRows.append(...rows);
  if (fresh && !rows.length) missingRows.append(el("tr", {}, el("td", { colspan: "6", class: "oem-sub", text: "Every part here has an OEM code." })));
  offset += data.items.length;
  document.querySelector("#missing-count").textContent = `${count(data.total)} parts`;
  moreButton.hidden = offset >= data.total;
}

filters.addEventListener("submit", (event) => {
  event.preventDefault();
  loadMissing(true).catch((error) => showError(error.message));
});
moreButton.addEventListener("click", () => loadMissing().catch((error) => showError(error.message)));

document.querySelector("#excel-upload").addEventListener("submit", async (event) => {
  event.preventDefault();
  uploadStatus.className = "alias-status";
  uploadStatus.textContent = "Uploading…";
  try {
    const result = await request("/api/admin/oem/upload", { method: "POST", body: new FormData(event.target) });
    const notes = [
      `${count(result.codes_added)} codes added to ${count(result.parts_updated)} parts`,
      result.already_there ? `${count(result.already_there)} were already there` : "",
      result.unknown_parts.length ? `unknown Part IDs: ${result.unknown_parts.slice(0, 10).join(", ")}` : "",
      result.invalid.length ? `not OEM codes (skipped): ${result.invalid.slice(0, 10).join("; ")}` : "",
    ].filter(Boolean);
    uploadStatus.textContent = `${notes.join(". ")}.`;
    uploadStatus.classList.add("is-ok");
    event.target.reset();
    await Promise.all([loadSummary(), loadMissing(true)]);
  } catch (error) {
    uploadStatus.textContent = error.message;
    uploadStatus.classList.add("is-error");
  }
});

Promise.all([loadSummary(), loadSuggestions(), loadMissing(true)]).catch((error) => showError(error.message));
