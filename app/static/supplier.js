const supplierId = location.pathname.split("/").filter(Boolean).at(-1);
const products = document.querySelector("#supplier-products");

const money = (value, currency) => value == null
  ? "Narx so‘rov bo‘yicha"
  : `${new Intl.NumberFormat("uz-UZ", { maximumFractionDigits: 0 }).format(Number(value))} ${currency}`;

fetch(`/api/v1/suppliers/${supplierId}`).then(async (response) => {
  if (!response.ok) throw new Error("Supplier topilmadi");
  return response.json();
}).then((supplier) => {
  document.title = `${supplier.name} · MegaParts`;
  document.querySelector("#supplier-name").textContent = supplier.name;
  const contact = document.querySelector("#supplier-contact");
  if (supplier.phone) {
    const link = document.createElement("a"); link.href = `tel:${supplier.phone}`; link.textContent = supplier.phone; contact.append(link);
  }
  if (supplier.telegram) {
    const link = document.createElement("a"); link.href = supplier.telegram.startsWith("http") ? supplier.telegram : `https://t.me/${supplier.telegram.replace(/^@/, "")}`; link.textContent = "Telegram"; contact.append(link);
  }
  if (supplier.address) contact.append(document.createTextNode(supplier.address));
  document.querySelector("#supplier-summary").textContent = `${supplier.active_offers_count} faol taklif · ${supplier.brands.join(", ") || "Brend ko‘rsatilmagan"}`;
  supplier.products.forEach((item) => {
    const node = document.createElement("article"); node.className = "supplier-product";
    const title = document.createElement("h3"); title.textContent = item.name;
    const meta = document.createElement("div"); meta.className = "supplier-meta";
    [item.brand, item.supplier_sku, money(item.price, item.currency), item.stock_qty == null ? "Mavjudligi noma’lum" : `${item.stock_qty} dona`, item.warehouse, item.freshness_status].filter(Boolean).forEach((value) => { const span = document.createElement("span"); span.textContent = value; meta.append(span); });
    node.append(title, meta); products.append(node);
  });
}).catch((error) => { document.querySelector("#supplier-name").textContent = error.message; });
