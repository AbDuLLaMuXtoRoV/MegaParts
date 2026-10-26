// A supplier's public page, in the language chosen on the catalog page.
const STRINGS = {
  uz: {
    back: "← Katalogga qaytish",
    eyebrow: "Sotuvchi",
    loading: "Yuklanmoqda…",
    notFound: "Sotuvchi topilmadi",
    offers: "ta faol taklif",
    lastList: (date) => `Oxirgi ro‘yxat: ${date}`,
    listed: (date) => `Ro‘yxatda: ${date}`,
    brandsTitle: "Brendlar",
    productsTitle: "Detallar",
    brand: "Brend",
    code: "Kod",
    call: "Qo‘ng‘iroq qilish",
    filter: "Shu sotuvchi detallaridan qidirish…",
    noMatch: "Topilmadi",
    moreBrands: (n) => `Yana ${n} ta`,
    noBrands: "Brend ko‘rsatilmagan",
    noBrand: "Brendsiz",
    priceOnRequest: "Narxini so‘rang",
    stockUnknown: "Borligini so‘rang",
    inStock: (n) => `${n} dona`,
    verified: "✓ Tekshirilgan sotuvchi",
    unverified: "Hujjatlari hali tekshirilmagan",
    reliability: (p, n) => `Ishonchlilik: ${p}% (${n} ta buyurtma)`,
    newSeller: "Yangi sotuvchi",
    hours: (h) => `Ish vaqti: ${h}`,
    map: "Xaritada ko‘rish",
    som: "so‘m",
    FRESH: "Hozirgina yangilangan",
    RECENT: "Bugun yangilangan",
    STALE: "Qoldiq ma’lumoti eskirgan",
    OUTDATED: "Narx eskirgan bo‘lishi mumkin",
    UNKNOWN: "Yangilanish vaqti noma’lum",
  },
  ru: {
    back: "← Вернуться в каталог",
    eyebrow: "Продавец",
    loading: "Загрузка…",
    notFound: "Продавец не найден",
    offers: "активных предложений",
    lastList: (date) => `Последний прайс: ${date}`,
    listed: (date) => `В прайсе: ${date}`,
    brandsTitle: "Бренды",
    productsTitle: "Детали",
    brand: "Бренд",
    code: "Код",
    call: "Позвонить",
    filter: "Поиск по деталям продавца…",
    noMatch: "Ничего не найдено",
    moreBrands: (n) => `Ещё ${n}`,
    noBrands: "Бренды не указаны",
    noBrand: "Без бренда",
    priceOnRequest: "Цена по запросу",
    stockUnknown: "Уточните наличие",
    inStock: (n) => `${n} шт.`,
    verified: "✓ Проверенный продавец",
    unverified: "Документы ещё не проверены",
    reliability: (p, n) => `Надёжность: ${p}% (заказов: ${n})`,
    newSeller: "Новый продавец",
    hours: (h) => `Часы работы: ${h}`,
    map: "На карте",
    som: "сум",
    FRESH: "Только что обновлено",
    RECENT: "Обновлено сегодня",
    STALE: "Данные о наличии устарели",
    OUTDATED: "Цена могла устареть",
    UNKNOWN: "Время обновления неизвестно",
  },
  en: {
    back: "← Back to the catalog",
    eyebrow: "Seller",
    loading: "Loading…",
    notFound: "Seller not found",
    offers: "active offers",
    lastList: (date) => `Last price list: ${date}`,
    listed: (date) => `Listed: ${date}`,
    brandsTitle: "Brands",
    productsTitle: "Parts",
    brand: "Brand",
    code: "Code",
    call: "Call",
    filter: "Search this seller's parts…",
    noMatch: "Nothing found",
    moreBrands: (n) => `${n} more`,
    noBrands: "No brands listed",
    noBrand: "No brand",
    priceOnRequest: "Price on request",
    stockUnknown: "Ask about stock",
    inStock: (n) => `${n} in stock`,
    verified: "✓ Verified seller",
    unverified: "Documents not checked yet",
    reliability: (p, n) => `Reliability: ${p}% (${n} orders)`,
    newSeller: "New seller",
    hours: (h) => `Hours: ${h}`,
    map: "Show on map",
    som: "UZS",
    FRESH: "Just updated",
    RECENT: "Updated today",
    STALE: "Stock data is old",
    OUTDATED: "Price may be outdated",
    UNKNOWN: "Last update unknown",
  },
};

const lang = (() => {
  try { return STRINGS[localStorage.getItem("megaparts_lang")] ? localStorage.getItem("megaparts_lang") : "uz"; } catch { return "uz"; }
})();
const t = (key, ...args) => {
  const value = STRINGS[lang][key] ?? STRINGS.en[key];
  return typeof value === "function" ? value(...args) : value;
};

document.documentElement.lang = lang;
const $ = (selector) => document.querySelector(selector);
$("#supplier-back").textContent = t("back");
$("#supplier-eyebrow").textContent = t("eyebrow");
$("#supplier-name").textContent = t("loading");
$("#supplier-brands-title").textContent = t("brandsTitle");
$("#supplier-products-title").textContent = t("productsTitle");
$("#supplier-filter").placeholder = t("filter");
$("#supplier-filter").setAttribute("aria-label", t("filter"));

function el(tag, attributes = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attributes).forEach(([key, value]) => {
    if (value === undefined || value === null || value === false) return;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else node.setAttribute(key, value === true ? "" : value);
  });
  node.append(...[].concat(children).filter((child) => child !== null && child !== undefined && child !== false));
  return node;
}

const supplierId = location.pathname.split("/").filter(Boolean).at(-1);
// So'm are whole; dollar prices keep their cents ("2,47 $").
const money = (value, currency) => {
  if (value == null) return t("priceOnRequest");
  if (!currency || currency === "UZS") return `${new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 }).format(Number(value))} ${t("som")}`;
  const amount = new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Number(value));
  return currency === "USD" ? `${amount} $` : `${amount} ${currency}`;
};
const formatDate = (value) => new Date(value).toLocaleDateString(lang === "en" ? "en-GB" : "ru-RU");
const brandLabel = (name) => CatalogText.brandName(name ? { name } : null) || t("noBrand");
const chip = (label, value, mono = false) => el("span", { class: "meta-chip" }, [
  el("span", { class: "meta-label", text: label }),
  el("strong", { class: mono ? "mono" : null, text: value }),
]);

// One row per part: the part, its brand and the seller's code, then price, stock and the list date.
function productRow(item) {
  // A list without prices or stock only says the seller has the part; it does not go out of date.
  const listedOnly = item.price == null && item.stock_qty == null;
  const freshness = listedOnly && item.updated_at ? t("listed", formatDate(item.updated_at)) : t(item.freshness_status);
  const row = el("a", { class: "supplier-product", href: `/part/${encodeURIComponent(item.id)}` }, [
    el("span", { class: "supplier-product-name", text: CatalogText.productName(item, lang) }),
    el("span", { class: "supplier-product-meta" }, [
      chip(t("brand"), brandLabel(item.brand)),
      item.supplier_sku ? chip(t("code"), item.supplier_sku, true) : null,
    ]),
    el("span", { class: "supplier-product-side" }, [
      el("strong", { class: "price", text: money(item.price, item.currency) }),
      el("span", { class: `stock ${item.stock_qty == null ? "stock-unknown" : "stock-in"}`, text: item.stock_qty == null ? t("stockUnknown") : t("inStock", item.stock_qty) }),
      el("span", { class: "muted supplier-product-date", text: freshness }),
    ]),
  ]);
  row.dataset.search = [CatalogText.productName(item, lang), item.name, item.brand, item.supplier_sku].filter(Boolean).join(" ").toLowerCase();
  return row;
}

fetch(`/api/v1/suppliers/${supplierId}`).then(async (response) => {
  if (!response.ok) throw new Error(t("notFound"));
  return response.json();
}).then((supplier) => {
  const trust = supplier.trust;
  const name = trust ? CatalogText.supplierName(trust, lang) : supplier.name;
  document.title = `${name} · MegaParts`;
  $("#supplier-name").textContent = name;

  $("#supplier-trust").append(...[
    trust ? el("span", { class: `supplier-badge${trust.verified ? " is-verified" : ""}`, text: trust.verified ? t("verified") : t("unverified") }) : null,
    trust ? el("span", { class: "supplier-badge", text: trust.reliability_score != null ? t("reliability", Math.round(Number(trust.reliability_score)), trust.reliability_sample) : t("newSeller") }) : null,
    trust?.work_hours ? el("span", { class: "supplier-badge", text: t("hours", trust.work_hours) }) : null,
    supplier.address ? el("span", { class: "supplier-badge", text: CatalogText.placeName(supplier.address, lang) }) : null,
  ].filter(Boolean));

  const telegram = supplier.telegram && (supplier.telegram.startsWith("http") ? supplier.telegram : `https://t.me/${supplier.telegram.replace(/^[@+]/, "")}`);
  $("#supplier-contact").append(...[
    supplier.phone ? el("a", { class: "primary-button", href: `tel:${supplier.phone}` }, [`${t("call")} · `, el("span", { class: "mono", text: supplier.phone })]) : null,
    telegram ? el("a", { class: "secondary-button", href: telegram, target: "_blank", rel: "noopener", text: "Telegram" }) : null,
    trust?.map_url ? el("a", { class: "secondary-button", href: trust.map_url, target: "_blank", rel: "noopener", text: t("map") }) : null,
  ].filter(Boolean));

  $("#supplier-stats").append(...[
    el("li", {}, [el("strong", { text: new Intl.NumberFormat("ru-RU").format(supplier.active_offers_count) }), ` ${t("offers")}`]),
    supplier.last_data_update ? el("li", { text: t("lastList", formatDate(supplier.last_data_update)) }) : null,
  ].filter(Boolean));

  // A seller with dozens of brands shows the first ones; the rest open on request.
  const BRANDS_SHOWN = 18;
  const brands = [...new Set(supplier.brands.map((brand) => brandLabel(brand)))];
  const brandChips = brands.map((brand, index) => el("span", { class: "brand-chip", text: brand, hidden: index >= BRANDS_SHOWN }));
  const more = brands.length > BRANDS_SHOWN
    ? el("button", { type: "button", class: "brand-more", text: t("moreBrands", brands.length - BRANDS_SHOWN) })
    : null;
  more?.addEventListener("click", () => {
    brandChips.forEach((chipNode) => { chipNode.hidden = false; });
    more.remove();
  });
  $("#supplier-brands").append(...(brands.length ? [...brandChips, more].filter(Boolean) : [el("span", { class: "muted", text: t("noBrands") })]));

  const rows = supplier.products.map(productRow);
  const empty = el("p", { class: "muted supplier-empty", text: t("noMatch"), hidden: true });
  $("#supplier-products").append(...rows, empty);
  const filter = () => {
    const words = $("#supplier-filter").value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    rows.forEach((row) => {
      const match = words.every((word) => row.dataset.search.includes(word));
      row.hidden = !match;
      shown += Number(match);
    });
    empty.hidden = shown > 0;
    $("#supplier-count").textContent = words.length ? `${shown} / ${rows.length}` : String(rows.length);
  };
  $("#supplier-filter").addEventListener("input", filter);
  filter();
}).catch((error) => { $("#supplier-name").textContent = error.message; });
