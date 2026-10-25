// A supplier's public page, in the language chosen on the catalog page.
const STRINGS = {
  uz: {
    back: "← Katalogga qaytish",
    eyebrow: "Sotuvchi",
    loading: "Yuklanmoqda…",
    notFound: "Sotuvchi topilmadi",
    summary: (n, brands) => `${n} ta faol taklif · ${brands}`,
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
    summary: (n, brands) => `Активных предложений: ${n} · ${brands}`,
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
    summary: (n, brands) => `${n} active offers · ${brands}`,
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
try { if (localStorage.getItem("megaparts_text_large") === "1") document.documentElement.classList.add("text-large"); } catch { /* optional */ }

document.documentElement.lang = lang;
document.querySelector("#supplier-back").textContent = t("back");
document.querySelector("#supplier-eyebrow").textContent = t("eyebrow");
document.querySelector("#supplier-name").textContent = t("loading");

const supplierId = location.pathname.split("/").filter(Boolean).at(-1);
const products = document.querySelector("#supplier-products");
const span = (text) => { const node = document.createElement("span"); node.textContent = text; return node; };
// So'm are whole; dollar prices keep their cents ("2,47 $").
const money = (value, currency) => {
  if (value == null) return t("priceOnRequest");
  if (!currency || currency === "UZS") return `${new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 }).format(Number(value))} ${t("som")}`;
  const amount = new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Number(value));
  return currency === "USD" ? `${amount} $` : `${amount} ${currency}`;
};
const brandLabel = (name) => CatalogText.brandName(name ? { name } : null) || t("noBrand");

fetch(`/api/v1/suppliers/${supplierId}`).then(async (response) => {
  if (!response.ok) throw new Error(t("notFound"));
  return response.json();
}).then((supplier) => {
  const trust = supplier.trust;
  const name = trust ? CatalogText.supplierName(trust, lang) : supplier.name;
  document.title = `${name} · MegaParts`;
  document.querySelector("#supplier-name").textContent = name;
  const contact = document.querySelector("#supplier-contact");
  if (supplier.phone) {
    const link = document.createElement("a"); link.href = `tel:${supplier.phone}`; link.textContent = supplier.phone; contact.append(link);
  }
  if (supplier.telegram) {
    const link = document.createElement("a"); link.href = supplier.telegram.startsWith("http") ? supplier.telegram : `https://t.me/${supplier.telegram.replace(/^@/, "")}`; link.textContent = "Telegram"; contact.append(link);
  }
  if (supplier.address) contact.append(span(CatalogText.placeName(supplier.address, lang)));
  if (trust) {
    [
      trust.verified ? t("verified") : t("unverified"),
      trust.reliability_score != null ? t("reliability", Math.round(Number(trust.reliability_score)), trust.reliability_sample) : t("newSeller"),
      trust.work_hours ? t("hours", trust.work_hours) : null,
    ].filter(Boolean).forEach((text) => contact.append(span(text)));
    if (trust.map_url) {
      const map = document.createElement("a"); map.href = trust.map_url; map.target = "_blank"; map.rel = "noopener"; map.textContent = t("map"); contact.append(map);
    }
  }
  const brands = supplier.brands.map((brand) => brandLabel(brand));
  document.querySelector("#supplier-summary").textContent = t("summary", supplier.active_offers_count, [...new Set(brands)].join(", ") || t("noBrands"));
  supplier.products.forEach((item) => {
    const node = document.createElement("article"); node.className = "supplier-product";
    const title = document.createElement("h3"); title.textContent = CatalogText.productName(item, lang);
    const meta = document.createElement("div"); meta.className = "supplier-meta";
    [
      brandLabel(item.brand),
      item.supplier_sku,
      money(item.price, item.currency),
      item.stock_qty == null ? t("stockUnknown") : t("inStock", item.stock_qty),
      item.warehouse,
      t(item.freshness_status),
    ].filter(Boolean).forEach((value) => meta.append(span(value)));
    node.append(title, meta); products.append(node);
  });
}).catch((error) => { document.querySelector("#supplier-name").textContent = error.message; });
