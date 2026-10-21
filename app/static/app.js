// ---------- Language ----------

const ruPlural = (n, one, few, many) => {
  const tens = n % 100;
  const ones = n % 10;
  if (ones === 1 && tens !== 11) return one;
  if (ones >= 2 && ones <= 4 && (tens < 12 || tens > 14)) return few;
  return many;
};

const STRINGS = {
  uz: {
    skipToContent: "Asosiy qismga o‘tish",
    language: "Til",
    largerText: "Katta harf",
    title: "Mashinangiz uchun kerakli detalni toping",
    subtitle: "Mashinangizni tanlang, so‘ng detal nomini yozing yoki pastdagi bo‘limlardan tanlang.",
    stepCar: "Mashinangiz",
    make: "Marka",
    model: "Model",
    generation: "Avlod (yillar)",
    chooseMake: "— Markani tanlang —",
    chooseMakeFirst: "Avval markani tanlang",
    allModels: "— Barcha modellar —",
    allGenerations: "— Barcha avlodlar —",
    clearCar: "Tozalash",
    carOptional: "Ixtiyoriy. Mashinani tanlasangiz, faqat unga mos detallar ko‘rsatiladi.",
    carChosen: (car) => `Tanlandi: ${car}. Faqat shu mashinaga mos detallar ko‘rsatiladi.`,
    showAllForCar: (n) => `Mashinamga mos barcha detallar (${n})`,
    stepPart: "Qanday detal kerak?",
    searchPlaceholder: "Masalan: kolodka, svecha yoki detal raqami",
    searchButton: "Qidirish",
    examples: "Masalan:",
    exampleQueries: ["svecha", "kolodka", "moy filtri", "Cobalt svecha"],
    sectionsTitle: "Yoki bo‘limni tanlang",
    sectionsLead: "Mashinaning qaysi qismi uchun detal kerak?",
    parts: (n) => `${n} ta detal`,
    comingSoon: "Tez orada",
    noneForCar: "Mashinangizga hozircha yo‘q",
    loading: "Qidirilmoqda…",
    searchUnavailable: "Qidiruv vaqtincha ishlamayapti. Birozdan so‘ng qayta urinib ko‘ring.",
    breadcrumbs: "Siz shu yerdasiz",
    home: "Barcha bo‘limlar",
    resultsFor: (q) => `“${q}” bo‘yicha natijalar`,
    partsForCar: (car) => `${car} uchun detallar`,
    found: (n) => `${n} ta topildi`,
    filterCar: "Mashina",
    filterSection: "Bo‘lim",
    filterWord: "So‘z",
    remove: (label) => `Olib tashlash: ${label}`,
    startOver: "Boshidan boshlash",
    chooseType: "Detal turini tanlang",
    narrowByType: "Detal turi bo‘yicha saralash",
    all: "Hammasi",
    notYet: "Hozircha mavjud emas",
    notForCarYet: "Mashinangiz uchun hozircha yo‘q",
    correctedTo: (fixed) => `“${fixed}” bo‘yicha natijalar ko‘rsatilmoqda`,
    youTyped: (typed) => `Siz “${typed}” deb yozdingiz.`,
    searchTyped: "Aynan shuni qidirish",
    suggestions: "Takliflar",
    suggestFix: "Balki shuni nazarda tutdingiz",
    suggestTypes: "Detal turlari",
    suggestParts: "Detallar",
    related: "O‘xshash natijalar",
    moreThanShown: (shown, total) => `Birinchi ${shown} ta ko‘rsatildi (jami ${total}). Aniqroq topish uchun detal turini tanlang.`,
    noResultsTitle: "Hech narsa topilmadi",
    noResultsText: "Boshqa so‘z bilan yozib ko‘ring yoki tanlovlarni olib tashlang.",
    emptySectionTitle: "Bu bo‘limda hozircha detal yo‘q",
    emptySectionText: "Bu detallar tez orada qo‘shiladi. Boshqa bo‘limni tanlang yoki detal nomini yozib qidiring.",
    searchAllSections: "Barcha bo‘limlardan qidirish",
    searchWithoutCar: "Mashina tanlovisiz qidirish",
    browseSections: "Bo‘limlarni ko‘rish",
    fitsYourCar: "Mashinangizga mos",
    fitsAll: "Barcha mashinalarga mos",
    fitsUnknown: "Mashina ko‘rsatilmagan",
    fits: "Mos keladi:",
    more: (n) => `yana ${n} ta`,
    noBrand: "Brendsiz",
    brand: "Brend",
    details: "Batafsil",
    priceOnRequest: "Narxini so‘rang",
    priceFrom: (price) => `${price} dan`,
    som: "so‘m",
    inStock: (n) => `Bor: ${n} dona`,
    outOfStock: "Tugagan",
    askStock: "Borligini so‘rang",
    back: "← Orqaga",
    partType: "Detal turi",
    position: "Joylashuvi",
    side: "Tomoni",
    origin: "Ishlab chiqarilgan",
    FRONT: "Old", REAR: "Orqa", LEFT: "Chap", RIGHT: "O‘ng", BOTH: "Ikkala tomon",
    fitsCarBanner: (car) => `Bu detal mashinangizga mos: ${car}.`,
    referenceNumbers: "Detal raqamlari",
    noReferences: "Detal raqami ko‘rsatilmagan.",
    fitments: "Qaysi mashinalarga mos",
    sellers: (n) => `Sotuvchilar (${n})`,
    noOffers: "Hozircha sotuvda yo‘q.",
    noSellerCode: "Sotuvchi kodi yo‘q",
    viewSeller: "Sotuvchini ko‘rish",
    call: "Qo‘ng‘iroq qilish",
    reserve: "Band qilish",
    reserveQty: "Nechta kerak?",
    reservePhone: "Telefon raqamingiz (ixtiyoriy)",
    send: "Yuborish",
    cancel: "Bekor qilish",
    reserveSent: "So‘rov yuborildi.",
    reserveError: "Yuborib bo‘lmadi. Qayta urinib ko‘ring.",
    testData: "Test ma’lumot",
    freshUnknown: "Yangilanish vaqti noma’lum",
    freshNow: "Hozirgina yangilangan",
    freshHours: (n) => `${n} soat oldin yangilangan`,
    stale: (n) => `Qoldiq ma’lumoti eskirgan · ${n} soat oldin`,
    productNotFound: "Detal topilmadi.",
    detailError: "Detal ma’lumotlarini yuklab bo‘lmadi.",
    feedbackLabel: "Fikringiz",
    feedbackFound: "Kerakli detalni topdingizmi?",
    feedbackTop: "Birinchi natijalarda chiqdimi?",
    feedbackRate: "Qidiruvni baholang (ixtiyoriy)",
    feedbackThanks: "Rahmat — javobingiz saqlandi.",
    yes: "Ha",
    no: "Yo‘q",
  },
  ru: {
    skipToContent: "Перейти к содержанию",
    language: "Язык",
    largerText: "Крупный шрифт",
    title: "Найдите нужную запчасть для вашей машины",
    subtitle: "Выберите машину, затем напишите название детали или выберите раздел ниже.",
    stepCar: "Ваша машина",
    make: "Марка",
    model: "Модель",
    generation: "Поколение (годы)",
    chooseMake: "— Выберите марку —",
    chooseMakeFirst: "Сначала выберите марку",
    allModels: "— Все модели —",
    allGenerations: "— Все поколения —",
    clearCar: "Сбросить",
    carOptional: "Необязательно. Если выберете машину, покажем только подходящие детали.",
    carChosen: (car) => `Показываем только детали, подходящие для ${car}.`,
    showAllForCar: (n) => `Все детали для моей машины (${n})`,
    stepPart: "Какая деталь нужна?",
    searchPlaceholder: "Например: колодки, свеча или номер детали",
    searchButton: "Найти",
    examples: "Например:",
    exampleQueries: ["свеча", "колодки", "фильтр масляный", "Кобальт свеча"],
    sectionsTitle: "Или выберите раздел",
    sectionsLead: "Для какой части машины нужна деталь?",
    parts: (n) => `${n} ${ruPlural(n, "деталь", "детали", "деталей")}`,
    comingSoon: "Скоро",
    noneForCar: "Для вашей машины пока нет",
    loading: "Ищем…",
    searchUnavailable: "Поиск временно недоступен. Попробуйте чуть позже.",
    breadcrumbs: "Вы здесь",
    home: "Все разделы",
    resultsFor: (q) => `Результаты по запросу «${q}»`,
    partsForCar: (car) => `Детали для ${car}`,
    found: (n) => `Найдено: ${n}`,
    filterCar: "Машина",
    filterSection: "Раздел",
    filterWord: "Запрос",
    remove: (label) => `Убрать: ${label}`,
    startOver: "Начать сначала",
    chooseType: "Выберите тип детали",
    narrowByType: "Уточнить по типу детали",
    all: "Все",
    notYet: "Пока нет в наличии",
    notForCarYet: "Для вашей машины пока нет",
    correctedTo: (fixed) => `Показываем результаты по «${fixed}»`,
    youTyped: (typed) => `Вы написали «${typed}».`,
    searchTyped: "Искать именно это",
    suggestions: "Подсказки",
    suggestFix: "Возможно, вы имели в виду",
    suggestTypes: "Типы деталей",
    suggestParts: "Детали",
    related: "Похожие результаты",
    moreThanShown: (shown, total) => `Показаны первые ${shown} из ${total}. Чтобы найти точнее, выберите тип детали.`,
    noResultsTitle: "Ничего не найдено",
    noResultsText: "Попробуйте другое слово или уберите выбранные фильтры.",
    emptySectionTitle: "В этом разделе пока нет деталей",
    emptySectionText: "Эти детали скоро появятся. Выберите другой раздел или найдите деталь по названию.",
    searchAllSections: "Искать во всех разделах",
    searchWithoutCar: "Искать без выбора машины",
    browseSections: "Смотреть разделы",
    fitsYourCar: "Подходит для вашей машины",
    fitsAll: "Подходит для всех машин",
    fitsUnknown: "Машина не указана",
    fits: "Подходит:",
    more: (n) => `ещё ${n}`,
    noBrand: "Без бренда",
    brand: "Бренд",
    details: "Подробнее",
    priceOnRequest: "Цена по запросу",
    priceFrom: (price) => `от ${price}`,
    som: "сум",
    inStock: (n) => `В наличии: ${n} шт.`,
    outOfStock: "Нет в наличии",
    askStock: "Уточните наличие",
    back: "← Назад",
    partType: "Тип детали",
    position: "Расположение",
    side: "Сторона",
    origin: "Происхождение",
    FRONT: "Передний", REAR: "Задний", LEFT: "Левый", RIGHT: "Правый", BOTH: "Обе стороны",
    fitsCarBanner: (car) => `Эта деталь подходит для вашей машины ${car}.`,
    referenceNumbers: "Номера деталей",
    noReferences: "Номер детали не указан.",
    fitments: "Подходит для машин",
    sellers: (n) => `Продавцы (${n})`,
    noOffers: "Сейчас нет в продаже.",
    noSellerCode: "Нет кода продавца",
    viewSeller: "О продавце",
    call: "Позвонить",
    reserve: "Забронировать",
    reserveQty: "Сколько штук нужно?",
    reservePhone: "Ваш телефон (необязательно)",
    send: "Отправить",
    cancel: "Отмена",
    reserveSent: "Заявка отправлена.",
    reserveError: "Не удалось отправить. Попробуйте ещё раз.",
    testData: "Тестовые данные",
    freshUnknown: "Время обновления неизвестно",
    freshNow: "Только что обновлено",
    freshHours: (n) => `Обновлено ${n} ч назад`,
    stale: (n) => `Данные о наличии устарели · ${n} ч назад`,
    productNotFound: "Деталь не найдена.",
    detailError: "Не удалось загрузить данные о детали.",
    feedbackLabel: "Ваш отзыв",
    feedbackFound: "Вы нашли нужную деталь?",
    feedbackTop: "Она была среди первых результатов?",
    feedbackRate: "Оцените поиск (необязательно)",
    feedbackThanks: "Спасибо — ответ сохранён.",
    yes: "Да",
    no: "Нет",
  },
  en: {
    skipToContent: "Skip to main content",
    language: "Language",
    largerText: "Larger text",
    title: "Find the right part for your car",
    subtitle: "Choose your car, then type the part name or pick a section below.",
    stepCar: "Your car",
    make: "Make",
    model: "Model",
    generation: "Generation (years)",
    chooseMake: "— Choose a make —",
    chooseMakeFirst: "Choose a make first",
    allModels: "— All models —",
    allGenerations: "— All generations —",
    clearCar: "Clear",
    carOptional: "Optional. Choose your car to see only the parts that fit it.",
    carChosen: (car) => `Showing only parts that fit ${car}.`,
    showAllForCar: (n) => `All parts for my car (${n})`,
    stepPart: "What part do you need?",
    searchPlaceholder: "For example: brake pads, spark plug or part number",
    searchButton: "Search",
    examples: "Try:",
    exampleQueries: ["spark plug", "brake pads", "oil filter", "fuel pump"],
    sectionsTitle: "Or choose a section",
    sectionsLead: "Which part of the car needs a part?",
    parts: (n) => `${n} ${n === 1 ? "part" : "parts"}`,
    comingSoon: "Coming soon",
    noneForCar: "None for your car yet",
    loading: "Searching…",
    searchUnavailable: "Search is temporarily unavailable. Please try again shortly.",
    breadcrumbs: "You are here",
    home: "All sections",
    resultsFor: (q) => `Results for “${q}”`,
    partsForCar: (car) => `Parts for ${car}`,
    found: (n) => `${n} found`,
    filterCar: "Car",
    filterSection: "Section",
    filterWord: "Search",
    remove: (label) => `Remove ${label}`,
    startOver: "Start over",
    chooseType: "Choose the part type",
    narrowByType: "Narrow down by part type",
    all: "All",
    notYet: "Not available yet",
    notForCarYet: "Not available for your car yet",
    correctedTo: (fixed) => `Showing results for “${fixed}”`,
    youTyped: (typed) => `You typed “${typed}”.`,
    searchTyped: "Search for exactly that",
    suggestions: "Suggestions",
    suggestFix: "Did you mean",
    suggestTypes: "Part types",
    suggestParts: "Parts",
    related: "Similar results",
    moreThanShown: (shown, total) => `Showing the first ${shown} of ${total}. Choose a part type to narrow it down.`,
    noResultsTitle: "Nothing found",
    noResultsText: "Try a different word or remove the filters you chose.",
    emptySectionTitle: "No parts in this section yet",
    emptySectionText: "These parts are coming soon. Choose another section or search by part name.",
    searchAllSections: "Search all sections",
    searchWithoutCar: "Search without the car filter",
    browseSections: "Browse sections",
    fitsYourCar: "Fits your car",
    fitsAll: "Fits all cars",
    fitsUnknown: "Car not specified",
    fits: "Fits:",
    more: (n) => `${n} more`,
    noBrand: "No brand",
    brand: "Brand",
    details: "Details",
    priceOnRequest: "Price on request",
    priceFrom: (price) => `from ${price}`,
    som: "UZS",
    inStock: (n) => `In stock: ${n}`,
    outOfStock: "Out of stock",
    askStock: "Ask about stock",
    back: "← Back",
    partType: "Part type",
    position: "Position",
    side: "Side",
    origin: "Origin",
    FRONT: "Front", REAR: "Rear", LEFT: "Left", RIGHT: "Right", BOTH: "Both sides",
    fitsCarBanner: (car) => `This part fits your ${car}.`,
    referenceNumbers: "Part numbers",
    noReferences: "No part number given.",
    fitments: "Fits these cars",
    sellers: (n) => `Sellers (${n})`,
    noOffers: "Not on sale right now.",
    noSellerCode: "No seller code",
    viewSeller: "View seller",
    call: "Call",
    reserve: "Reserve",
    reserveQty: "How many do you need?",
    reservePhone: "Your phone number (optional)",
    send: "Send",
    cancel: "Cancel",
    reserveSent: "Request sent.",
    reserveError: "Could not send. Please try again.",
    testData: "Test data",
    freshUnknown: "Last update unknown",
    freshNow: "Just updated",
    freshHours: (n) => `Updated ${n} h ago`,
    stale: (n) => `Stock data is old · ${n} h ago`,
    productNotFound: "Part not found.",
    detailError: "Could not load part details.",
    feedbackLabel: "Your feedback",
    feedbackFound: "Did you find the part you needed?",
    feedbackTop: "Was it among the first results?",
    feedbackRate: "Rate the search (optional)",
    feedbackThanks: "Thank you — your answer was saved.",
    yes: "Yes",
    no: "No",
  },
};

const storage = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  // Per-browser conveniences only; the page works without them.
  set(key, value) { try { localStorage.setItem(key, value); } catch { /* ignore */ } },
};

const pickLanguage = () => {
  const saved = storage.get("megaparts_lang");
  if (STRINGS[saved]) return saved;
  const browser = (navigator.language || "").slice(0, 2).toLowerCase();
  return STRINGS[browser] ? browser : "uz";
};

let lang = pickLanguage();
const t = (key, ...args) => {
  const value = STRINGS[lang][key] ?? STRINGS.en[key];
  return typeof value === "function" ? value(...args) : value;
};
const localName = (category) => (category ? category[`name_${lang}`] || category.name_uz : "");

// ---------- Elements and state ----------

const $ = (selector) => document.querySelector(selector);
const form = $("#search-form");
const input = $("#search-input");
const browseView = $("#browse-view");
const groupGrid = $("#group-grid");
const loading = $("#loading");
const errorBox = $("#error");
const resultsView = $("#results-view");
const detailView = $("#detail-view");
const results = $("#results");
const noResults = $("#no-results");
const resultsMore = $("#results-more");
const typeFilter = $("#type-filter");
const activeFilters = $("#active-filters");
const breadcrumbs = $("#breadcrumbs");
const spellingNotice = $("#spelling-notice");
const carMake = $("#car-make");
const carModel = $("#car-model");
const carGeneration = $("#car-generation");
const generationField = $("#generation-field");
const carClear = $("#car-clear");
const carHint = $("#car-hint");
const content = $("#content");

const PAGE_SIZE = 100;
const state = { query: "", category: "", all: false, spellcheck: true };
let lastResponse = null;
let lastResponseUrl = "";
let lastDetail = null;
let searchSeq = 0;
let currentEventId = null;
let currentProductId = null;
let pilotMode = false;
let vehicles = [];
let groupsAll = [];
let groupsForCar = null;
const categoryIndex = new Map();

fetch("/api/pilot-config").then((response) => response.json()).then((data) => { pilotMode = data.pilot_mode; }).catch(() => {});

const newId = () => (crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`);
let pilotSessionId = storage.get("megaparts_pilot_session");
if (!pilotSessionId) {
  pilotSessionId = newId();
  storage.set("megaparts_pilot_session", pilotSessionId);
}

const readStoredCar = () => {
  try { return JSON.parse(storage.get("megaparts_car")) || {}; } catch { return {}; }
};
let car = readStoredCar();
const hasCar = () => Boolean(car.make);
const carLabel = () => {
  if (car.vehicle_id) {
    const vehicle = vehicles.find((entry) => entry.id === car.vehicle_id);
    if (vehicle) return [vehicle.make, vehicle.model, vehicle.generation].filter(Boolean).join(" ");
  }
  return [car.make, car.model].filter(Boolean).join(" ");
};
const carParams = (params) => {
  if (car.vehicle_id) params.set("vehicle_id", car.vehicle_id);
  else if (car.make) {
    params.set("make", car.make);
    if (car.model) params.set("model", car.model);
  }
  return params;
};

// ---------- Small helpers ----------

function el(tag, attributes = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attributes).forEach(([key, value]) => {
    if (value === undefined || value === null || value === false) return;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key === "onclick") node.addEventListener("click", value);
    else node.setAttribute(key, value === true ? "" : value);
  });
  node.append(...[].concat(children).filter((child) => child !== null && child !== undefined && child !== false));
  return node;
}

const postJson = (url, payload) => fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload),
});

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const scrollToContent = () => {
  const top = content.getBoundingClientRect().top;
  if (top < 0 || top > window.innerHeight * 0.5) {
    content.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
  }
};

const formatNumber = (value) => new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 }).format(Number(value));
const formatPrice = (value, currency) => `${formatNumber(value)} ${!currency || currency === "UZS" ? t("som") : currency}`;

const ICONS = {
  "CAT-ENG": '<path d="M4 10v5M4 12.5h2M6 9h3V7h5v2h2l2 2h2v5h-2l-2 2H9l-3-2z"/><path d="M9 5h5"/>',
  "CAT-FLT": '<path d="M3 5h18l-7 8v5l-4 2v-7z"/>',
  "CAT-OIL": '<path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z"/><path d="M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5"/>',
  "CAT-BRK": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.5"/><path d="M16.5 4.5a9.5 9.5 0 0 1 3 3.5"/>',
  "CAT-SUS": '<path d="M8 3h8M8 21h8M8 6l8 2-8 2 8 2-8 2 8 2-8 2"/>',
  "CAT-STR": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2"/><path d="M3.5 10.5H10M14 10.5h6.5M12 14v7"/>',
  "CAT-IGN": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
  "CAT-FUEL": '<path d="M4 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M3 21h12M6.5 8h5M14 10h2a2 2 0 0 1 2 2v4a1.5 1.5 0 0 0 3 0V8l-3-3"/>',
  "CAT-COOL": '<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/><path d="M12 10v7"/>',
  "CAT-EL": '<rect x="3" y="7" width="18" height="12" rx="2"/><path d="M7 7V5M17 7V5M6.5 13h3M14.5 13h3M16 11.5v3"/>',
  "CAT-DRV": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9 7 7M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
  "CAT-EXH": '<path d="M2 15h10l3-2h4v6h-4l-3-2H2"/><path d="M6 10c0-1.5 2-1.5 2-3M11 10c0-1.5 2-1.5 2-3"/>',
  "CAT-BODY": '<path d="M3 16v-3l2-5a2 2 0 0 1 2-1h10a2 2 0 0 1 2 1l2 5v3z"/><circle cx="7.5" cy="16.5" r="2"/><circle cx="16.5" cy="16.5" r="2"/><path d="M4 12h16"/>',
  "CAT-CHEM": '<path d="M8 9h7v12H8zM9.5 9V6h4v3M13.5 6H17l2-2M19 7.5l1.5.5M18 10l1.5 1"/>',
  "CAT-ACC": '<path d="M14.5 5.5a4 4 0 0 0 4.9 4.9L21 12l-9 9-3-3 9-9-1.6-1.6a4 4 0 0 1-4.9-4.9L14 1.5z"/>',
};
const icon = (id) => `<svg viewBox="0 0 24 24" aria-hidden="true">${ICONS[id] || '<rect x="4" y="4" width="16" height="16" rx="3"/>'}</svg>`;

// ---------- Part groups ----------

function indexCategories() {
  categoryIndex.clear();
  groupsAll.forEach((group) => {
    categoryIndex.set(group.id, { node: group, group });
    group.types.forEach((type) => categoryIndex.set(type.id, { node: type, group }));
  });
}

const countsOf = (groups) => {
  const counts = new Map();
  (groups || []).forEach((group) => {
    counts.set(group.id, group.part_count);
    group.types.forEach((type) => counts.set(type.id, type.part_count));
  });
  return counts;
};
// Counts for the chosen car once they have loaded, otherwise for the whole catalog.
const carCounts = () => countsOf(hasCar() && groupsForCar ? groupsForCar : groupsAll);

async function loadGroups() {
  try {
    const response = await fetch("/api/v1/part-groups");
    if (response.ok) groupsAll = await response.json();
  } catch { /* the search box still works without the sections */ }
  indexCategories();
  await loadCarGroups();
}

async function loadCarGroups() {
  groupsForCar = null;
  if (!hasCar()) return;
  try {
    const response = await fetch(`/api/v1/part-groups?${carParams(new URLSearchParams())}`);
    if (response.ok) groupsForCar = await response.json();
  } catch { /* fall back to catalog-wide counts */ }
}

function renderGroups() {
  const counts = carCounts();
  const totals = countsOf(groupsAll);
  groupGrid.replaceChildren(...groupsAll.map((group) => {
    const count = counts.get(group.id) || 0;
    const tile = el("button", { type: "button", class: `group-tile${count ? "" : " is-empty"}`, onclick: () => navigate({ query: "", category: group.id }) });
    tile.innerHTML = `<span class="group-icon">${icon(group.id)}</span><span class="group-text"><span class="group-name"></span><span class="group-count"></span></span><span class="group-arrow" aria-hidden="true">›</span>`;
    tile.querySelector(".group-name").textContent = localName(group);
    tile.querySelector(".group-count").textContent = count ? t("parts", count) : totals.get(group.id) ? t("noneForCar") : t("comingSoon");
    return tile;
  }));
}

// ---------- Car ----------

const option = (value, label) => el("option", { value, text: label });

function fillSelect(select, placeholder, entries, selected) {
  select.replaceChildren(option("", placeholder), ...entries.map(([value, label]) => option(value, label)));
  select.value = entries.some(([value]) => value === selected) ? selected : "";
}

function renderGarage() {
  const makes = [...new Set(vehicles.map((vehicle) => vehicle.make))];
  fillSelect(carMake, t("chooseMake"), makes.map((make) => [make, make]), car.make);
  const ofMake = vehicles.filter((vehicle) => vehicle.make === carMake.value);
  const models = [...new Set(ofMake.map((vehicle) => vehicle.model))];
  fillSelect(carModel, carMake.value ? t("allModels") : t("chooseMakeFirst"), models.map((model) => [model, model]), car.model);
  carModel.disabled = !models.length;
  const generations = ofMake.filter((vehicle) => vehicle.model === carModel.value);
  generationField.hidden = generations.length < 2;
  fillSelect(carGeneration, t("allGenerations"), generations.map((vehicle) => [vehicle.id, vehicle.generation || "—"]), car.vehicle_id);
  carClear.hidden = !hasCar();
  renderCarHint();
}

function renderCarHint() {
  carHint.replaceChildren();
  carHint.classList.toggle("is-chosen", hasCar());
  if (!hasCar()) {
    carHint.append(el("span", { text: t("carOptional") }));
    return;
  }
  carHint.append(el("span", { class: "check", "aria-hidden": "true", text: "✓" }), el("span", { text: t("carChosen", carLabel()) }));
  const total = groupsForCar ? groupsForCar.reduce((sum, group) => sum + group.part_count, 0) : 0;
  if (total) {
    carHint.append(el("button", { type: "button", class: "link-button", text: t("showAllForCar", total), onclick: () => navigate({ query: "", category: "", all: true }) }));
  }
}

async function setCar(next) {
  car = next;
  storage.set("megaparts_car", JSON.stringify(car));
  lastResponseUrl = ""; // cached results were for the previous car
  renderGarage();
  await loadCarGroups();
  renderCarHint();
  renderGroups();
  if (!detailView.hidden && lastDetail) renderDetail();
  else if (!resultsView.hidden || !loading.hidden) navigate({ ...state, push: false });
}

carMake.addEventListener("change", () => setCar(carMake.value ? { make: carMake.value } : {}));
carModel.addEventListener("change", () => setCar(carModel.value ? { make: car.make, model: carModel.value } : { make: car.make }));
carGeneration.addEventListener("change", () => setCar(carGeneration.value ? { ...car, vehicle_id: carGeneration.value } : { make: car.make, model: car.model }));
carClear.addEventListener("click", () => setCar({}));

// ---------- Views ----------

const showOnly = (element) => {
  [browseView, loading, errorBox, resultsView, detailView].forEach((node) => { node.hidden = node !== element; });
};

const urlFor = (product) => {
  const params = new URLSearchParams();
  if (state.query) params.set("q", state.query);
  if (state.category) params.set("cat", state.category);
  if (state.all && !state.query && !state.category) params.set("all", "1");
  if (product) params.set("product", product);
  const search = params.toString();
  return search ? `/?${search}` : "/";
};

function showHome(push = true) {
  Object.assign(state, { query: "", category: "", all: false, spellcheck: true });
  input.value = "";
  if (push) history.pushState(null, "", "/");
  renderGroups();
  showOnly(browseView);
}

function navigate({ query = state.query, category = state.category, all = false, spellcheck = true, push = true } = {}) {
  Object.assign(state, { query: query.trim(), category, all, spellcheck });
  if (!state.query && !state.category && !(state.all && hasCar())) {
    showHome(push);
    return;
  }
  runSearch({ push });
}

async function runSearch({ push = true } = {}) {
  const requestId = ++searchSeq;
  input.value = state.query;
  currentEventId = null;
  if (push) history.pushState(null, "", urlFor());
  showOnly(loading);
  scrollToContent();
  const params = new URLSearchParams({ q: state.query, limit: String(PAGE_SIZE), session_id: pilotSessionId });
  carParams(params);
  if (state.category) params.set("category", state.category);
  if (!state.spellcheck) params.set("spellcheck", "false");
  try {
    const response = await fetch(`/api/v1/search?${params}`);
    if (requestId !== searchSeq) return;
    if (!response.ok) throw new Error(t("searchUnavailable"));
    lastResponse = await response.json();
    lastResponseUrl = urlFor();
    currentEventId = lastResponse.search_event_id;
    renderResults();
  } catch (error) {
    if (requestId !== searchSeq) return;
    errorBox.textContent = error.message;
    showOnly(errorBox);
  }
}

const lookupCategory = (id) => categoryIndex.get(id)?.node
  || lastResponse?.items.find((item) => item.category?.id === id)?.category
  || (lastResponse?.category_filter?.id === id ? lastResponse.category_filter : null);

function renderBreadcrumbs() {
  const crumbs = [el("button", { type: "button", class: "crumb", text: t("home"), onclick: () => showHome() })];
  const entry = categoryIndex.get(state.category);
  if (entry) {
    crumbs.push(el("button", { type: "button", class: "crumb", text: localName(entry.group), onclick: () => navigate({ query: "", category: entry.group.id }) }));
    if (entry.node !== entry.group) crumbs.push(el("span", { class: "crumb is-current", "aria-current": "page", text: localName(entry.node) }));
    else crumbs[crumbs.length - 1].setAttribute("aria-current", "page");
  }
  breadcrumbs.replaceChildren(...crumbs.flatMap((crumb, index) => (index ? [el("span", { class: "crumb-separator", "aria-hidden": "true", text: "›" }), crumb] : [crumb])));
}

function renderActiveFilters() {
  const chips = [];
  const chip = (label, value, onRemove) => el("span", { class: "filter-chip" }, [
    el("span", {}, [`${label}: `, el("strong", { text: value })]),
    el("button", { type: "button", class: "chip-remove", "aria-label": t("remove", value), title: t("remove", value), text: "✕", onclick: onRemove }),
  ]);
  if (hasCar() && lastResponse?.vehicle_filter) chips.push(chip(t("filterCar"), carLabel(), () => setCar({})));
  if (state.category) chips.push(chip(t("filterSection"), localName(lookupCategory(state.category)) || state.category, () => navigate({ category: "" })));
  if (state.query) chips.push(chip(t("filterWord"), state.query, () => navigate({ query: "" })));
  if (state.query || state.category) {
    chips.push(el("button", { type: "button", class: "link-button", text: t("startOver"), onclick: () => showHome() }));
  }
  activeFilters.replaceChildren(...chips);
  activeFilters.hidden = !chips.length;
}

function typePill(label, count, active, onClick) {
  return el("button", { type: "button", class: `type-pill${active ? " is-active" : ""}`, "aria-pressed": String(active), onclick: onClick }, [
    el("span", { text: label }),
    count === null ? null : el("span", { class: "pill-count", text: String(count) }),
  ]);
}

function renderTypeFilter() {
  typeFilter.replaceChildren();
  const entry = categoryIndex.get(state.category);
  if (!state.query && entry) {
    // Browsing a section: offer every part type in it.
    const { group } = entry;
    const counts = carCounts();
    const available = group.types.filter((type) => counts.get(type.id));
    const missing = group.types.filter((type) => !counts.get(type.id));
    if (available.length) {
      typeFilter.append(
        el("h3", { class: "filter-title", text: t("chooseType") }),
        el("div", { class: "pill-row" }, [
          typePill(t("all"), counts.get(group.id) || 0, state.category === group.id, () => navigate({ category: group.id })),
          ...available.map((type) => typePill(localName(type), counts.get(type.id), state.category === type.id, () => navigate({ category: type.id }))),
        ]),
      );
    }
    if (missing.length) {
      typeFilter.append(el("p", { class: "not-yet" }, [
        el("strong", { text: `${hasCar() ? t("notForCarYet") : t("notYet")}: ` }),
        missing.map(localName).join(", "),
      ]));
    }
    return;
  }
  const facets = Object.entries(lastResponse.category_counts || {}).sort((a, b) => b[1] - a[1]);
  if (state.query && (facets.length > 1 || state.category)) {
    typeFilter.append(
      el("h3", { class: "filter-title", text: t("narrowByType") }),
      el("div", { class: "pill-row" }, [
        typePill(t("all"), state.category ? null : lastResponse.total, !state.category, () => navigate({ category: "" })),
        ...facets.map(([id, count]) => typePill(localName(lookupCategory(id)) || id, count, state.category === id, () => navigate({ category: id }))),
      ]),
    );
  }
}

function renderSpelling() {
  spellingNotice.replaceChildren();
  spellingNotice.hidden = !lastResponse.corrected_query;
  if (!lastResponse.corrected_query) return;
  spellingNotice.append(
    el("span", { class: "spelling-icon", "aria-hidden": "true", text: "✎" }),
    el("span", {}, [
      el("strong", { text: t("correctedTo", lastResponse.corrected_query) }),
      `${t("youTyped", lastResponse.query)} `,
      el("button", { type: "button", class: "link-button", text: t("searchTyped"), onclick: () => navigate({ query: lastResponse.query, spellcheck: false }) }),
    ]),
  );
}

function renderNoResults() {
  const browsing = !state.query && state.category;
  const actions = [];
  if (state.query && state.category) actions.push(el("button", { type: "button", class: "primary-button", text: t("searchAllSections"), onclick: () => navigate({ category: "" }) }));
  if (lastResponse.vehicle_filter) actions.push(el("button", { type: "button", class: "secondary-button", text: t("searchWithoutCar"), onclick: () => setCar({}) }));
  actions.push(el("button", { type: "button", class: "secondary-button", text: t("browseSections"), onclick: () => showHome() }));
  noResults.replaceChildren(
    el("h3", { text: browsing ? t("emptySectionTitle") : t("noResultsTitle") }),
    el("p", { text: browsing ? t("emptySectionText") : t("noResultsText") }),
    el("div", { class: "no-results-actions" }, actions),
  );
}

function renderResults() {
  const data = lastResponse;
  const title = $("#results-title");
  if (data.query) title.textContent = t("resultsFor", data.corrected_query || data.query);
  else if (state.category) title.textContent = localName(lookupCategory(state.category));
  else title.textContent = t("partsForCar", carLabel());
  $("#results-count").textContent = t("found", data.total);
  renderBreadcrumbs();
  renderActiveFilters();
  renderTypeFilter();
  renderSpelling();

  results.replaceChildren();
  let relatedShown = false;
  data.items.forEach((item) => {
    if (item.result_group === "RELATED" && data.query && !relatedShown) {
      results.append(el("h3", { class: "related-heading", text: t("related") }));
      relatedShown = true;
    }
    results.append(resultCard(item, Boolean(data.vehicle_filter)));
  });
  noResults.hidden = data.total > 0;
  if (!data.total) renderNoResults();
  resultsMore.hidden = data.total <= data.items.length;
  resultsMore.textContent = resultsMore.hidden ? "" : t("moreThanShown", data.items.length, data.total);
  showOnly(resultsView);
}

const placeLabel = (item) => [item.position, item.side].filter(Boolean).map((value) => t(value) || value).join(" · ");

function priceSummary(offers) {
  const prices = offers.map((offer) => offer.price).filter((price) => price !== null && price !== undefined).map(Number);
  if (!prices.length) return { text: t("priceOnRequest"), known: false };
  const lowest = Math.min(...prices);
  const text = formatPrice(lowest, offers.find((offer) => Number(offer.price) === lowest)?.currency);
  return { text: new Set(prices).size > 1 ? t("priceFrom", text) : text, known: true };
}

function stockSummary(offers) {
  const known = offers.filter((offer) => offer.stock_qty !== null && offer.stock_qty !== undefined);
  if (!known.length) return { text: t("askStock"), tone: "unknown" };
  const quantity = known.reduce((sum, offer) => sum + Math.max(0, offer.stock_qty), 0);
  return quantity > 0 ? { text: t("inStock", quantity), tone: "in" } : { text: t("outOfStock"), tone: "out" };
}

function fitSummary(item) {
  if (item.universal) return t("fitsAll");
  const cars = [...new Set(item.vehicle_fitments.map((fitment) => [fitment.vehicle.make, fitment.vehicle.model].filter(Boolean).join(" ")))];
  if (!cars.length) return t("fitsUnknown");
  return `${t("fits")} ${cars.slice(0, 2).join(", ")}${cars.length > 2 ? `, ${t("more", cars.length - 2)}` : ""}`;
}

function resultCard(item, fitsCar) {
  const offers = item.offers || item.supplier_offers;
  const price = priceSummary(offers);
  const stock = stockSummary(offers);
  const place = placeLabel(item);
  const open = async () => {
    currentProductId = item.id;
    if (currentEventId) {
      try { await postJson(`/api/search-events/${currentEventId}/click`, { product_id: item.id }); } catch { /* analytics only */ }
    }
    openProduct(item.id);
  };
  const card = el("article", { class: "result-card", onclick: open }, [
    el("p", { class: "result-type", text: localName(item.category) }),
    el("h3", { class: "result-name", text: item.name }),
    el("p", { class: "result-brand" }, [`${t("brand")}: `, el("strong", { text: item.brand?.name || t("noBrand") })]),
    place ? el("p", { class: "result-place", text: place }) : null,
    fitsCar && !item.universal
      ? el("p", { class: "result-fit is-match" }, [el("span", { "aria-hidden": "true", text: "✓ " }), t("fitsYourCar")])
      : el("p", { class: `result-fit${item.universal ? " is-match" : ""}`, text: fitSummary(item) }),
    el("div", { class: "result-bottom" }, [
      el("div", {}, [
        el("div", { class: `result-price${price.known ? "" : " is-unknown"}`, text: price.text }),
        el("div", { class: `stock stock-${stock.tone}`, text: stock.text }),
      ]),
      el("button", { type: "button", class: "details-button", text: `${t("details")} →` }),
    ]),
  ]);
  return card;
}

// ---------- Product detail ----------

async function openProduct(id, push = true) {
  showOnly(loading);
  scrollToContent();
  if (push) history.pushState(null, "", urlFor(id));
  try {
    const response = await fetch(`/api/v1/products/${encodeURIComponent(id)}`);
    if (!response.ok) throw new Error(response.status === 404 ? t("productNotFound") : t("detailError"));
    lastDetail = await response.json();
    renderDetail();
  } catch (error) {
    errorBox.textContent = error.message;
    showOnly(errorBox);
  }
}

const freshnessLabel = (offer) => {
  if (offer.freshness_status === "UNKNOWN" || !offer.updated_at) return t("freshUnknown");
  const hours = Math.max(0, Math.round((Date.now() - new Date(offer.updated_at).getTime()) / 3600000));
  if (offer.freshness_status === "FRESH") return hours < 1 ? t("freshNow") : t("freshHours", hours);
  if (offer.freshness_status === "RECENT") return t("freshHours", hours);
  return t("stale", hours);
};

const recordAction = (action, offer) => {
  if (!currentEventId || !pilotMode) return Promise.resolve();
  return postJson(`/api/search-events/${currentEventId}/action`, {
    action,
    product_id: currentProductId,
    supplier_id: offer.supplier.id,
    supplier_offer_id: offer.id,
  }).catch(() => {});
};

const fitsChosenCar = (item) => hasCar() && (item.universal || item.vehicle_fitments.some(({ vehicle }) => (car.vehicle_id
  ? vehicle.id === car.vehicle_id
  : vehicle.make === car.make && (!car.model || vehicle.model === car.model))));

function feedbackPanel() {
  const panel = el("section", { class: "pilot-feedback" });
  const heading = el("h3", { text: t("feedbackFound") });
  const actions = el("div", { class: "feedback-actions" });
  panel.append(el("p", { class: "pilot-label", text: t("feedbackLabel") }), heading, actions);
  const submit = async (feedback) => {
    await postJson(`/api/search-events/${currentEventId}/feedback`, feedback);
    heading.textContent = t("feedbackRate");
    actions.replaceChildren(...[1, 2, 3, 4, 5].map((rating) => el("button", {
      type: "button",
      class: "rating",
      text: String(rating),
      onclick: async () => {
        await postJson(`/api/search-events/${currentEventId}/feedback`, { ...feedback, user_rating: rating });
        panel.replaceChildren(el("p", { class: "feedback-thanks", text: t("feedbackThanks") }));
      },
    })));
  };
  actions.append(
    el("button", {
      type: "button",
      text: t("yes"),
      onclick: () => {
        heading.textContent = t("feedbackTop");
        actions.replaceChildren(
          el("button", { type: "button", text: t("yes"), onclick: () => submit({ found_correct_part: true, correct_in_top_3: true }) }),
          el("button", { type: "button", text: t("no"), onclick: () => submit({ found_correct_part: true, correct_in_top_3: false }) }),
        );
      },
    }),
    el("button", { type: "button", text: t("no"), onclick: () => submit({ found_correct_part: false, correct_in_top_3: false }) }),
  );
  return panel;
}

function reserveForm(offer, toggle) {
  const quantity = el("input", { type: "number", min: "1", step: "1", value: "1", required: true, inputmode: "numeric" });
  const phone = el("input", { type: "tel", autocomplete: "tel" });
  const status = el("p", { class: "reserve-status", role: "status" });
  const formNode = el("form", { class: "reserve-form", hidden: true }, [
    el("label", { class: "field" }, [el("span", { class: "field-label", text: t("reserveQty") }), quantity]),
    el("label", { class: "field" }, [el("span", { class: "field-label", text: t("reservePhone") }), phone]),
    el("div", { class: "reserve-actions" }, [
      el("button", { type: "submit", class: "primary-button", text: t("send") }),
      el("button", { type: "button", class: "secondary-button", text: t("cancel"), onclick: () => { formNode.hidden = true; toggle.hidden = false; } }),
    ]),
    status,
  ]);
  formNode.addEventListener("submit", async (event) => {
    event.preventDefault();
    const amount = Number(quantity.value);
    if (!Number.isInteger(amount) || amount < 1) return;
    let ok = false;
    try {
      const response = await postJson("/api/v1/reservations", { session_id: pilotSessionId, search_event_id: currentEventId, product_id: currentProductId, supplier_offer_id: offer.id, quantity: amount, phone: phone.value.trim() || null });
      ok = response.ok;
    } catch { /* reported below */ }
    status.textContent = ok ? t("reserveSent") : t("reserveError");
    status.className = `reserve-status ${ok ? "is-ok" : "is-error"}`;
    if (ok) formNode.querySelectorAll("input, button").forEach((node) => { node.disabled = true; });
  });
  return formNode;
}

function offerNode(offer) {
  const price = offer.price === null || offer.price === undefined ? t("priceOnRequest") : formatPrice(offer.price, offer.currency);
  const stock = stockSummary([offer]);
  const reserveButton = el("button", { type: "button", class: "primary-button", text: t("reserve") });
  const formNode = reserveForm(offer, reserveButton);
  reserveButton.addEventListener("click", () => { reserveButton.hidden = true; formNode.hidden = false; formNode.querySelector("input").focus(); });
  const actions = [
    el("button", { type: "button", class: "secondary-button", text: t("viewSeller"), onclick: async () => { await recordAction("supplier_click", offer); location.href = `/suppliers/${offer.supplier.id}`; } }),
  ];
  if (offer.supplier.phone) {
    actions.push(el("button", { type: "button", class: "secondary-button", text: t("call"), onclick: async () => { await recordAction("phone_click", offer); location.href = `tel:${offer.supplier.phone}`; } }));
  }
  if (offer.supplier.telegram) {
    const telegram = offer.supplier.telegram;
    actions.push(el("button", { type: "button", class: "secondary-button", text: "Telegram", onclick: async () => {
      await recordAction("telegram_click", offer);
      location.href = telegram.startsWith("http") ? telegram : `https://t.me/${telegram.replace(/^@/, "")}`;
    } }));
  }
  actions.push(reserveButton);
  recordAction("supplier_offer_view", offer);
  return el("div", { class: "offer" }, [
    el("div", { class: "offer-supplier", text: offer.supplier.name }),
    el("div", { class: "offer-code", text: offer.supplier_sku || t("noSellerCode") }),
    el("div", { class: "offer-row" }, [el("span", { class: "price", text: price }), el("span", { class: `stock stock-${stock.tone}`, text: stock.text })]),
    el("div", { class: "offer-freshness", text: freshnessLabel(offer) }),
    pilotMode && offer.data_status === "DEMO" ? el("div", { class: "offer-demo", text: t("testData") }) : null,
    el("div", { class: "offer-actions" }, actions),
    formNode,
  ]);
}

function renderDetail() {
  const item = lastDetail;
  currentProductId = item.id;
  const back = el("button", {
    type: "button",
    class: "back secondary-button",
    text: t("back"),
    onclick: () => (lastResponse ? history.back() : showHome()),
  });

  const facts = [[t("partType"), localName(item.category)], [t("position"), item.position && (t(item.position) || item.position)], [t("side"), item.side && (t(item.side) || item.side)], [t("origin"), item.origin]]
    .filter(([, value]) => value)
    .map(([label, value]) => el("div", { class: "fact" }, [el("span", { text: label }), el("strong", { text: value })]));

  const references = item.reference_numbers.length
    ? item.reference_numbers.map((ref) => el("span", { class: "reference", text: ref.number }))
    : [el("p", { class: "muted", text: t("noReferences") })];

  const cars = item.universal
    ? [el("div", { class: "fitment is-match", text: t("fitsAll") })]
    : item.vehicle_fitments.length
      ? item.vehicle_fitments.map((fitment) => el("div", { class: "fitment", text: [fitment.vehicle.make, fitment.vehicle.model, fitment.vehicle.generation].filter(Boolean).join(" · ") }))
      : [el("p", { class: "muted", text: t("fitsUnknown") })];

  const main = el("article", { class: "detail-main" }, [
    el("div", { class: "detail-brand", text: item.brand?.name || t("noBrand") }),
    el("h2", { text: item.name }),
    fitsChosenCar(item) ? el("p", { class: "fit-banner" }, [el("span", { "aria-hidden": "true", text: "✓ " }), t("fitsCarBanner", carLabel())]) : null,
    facts.length ? el("div", { class: "facts" }, facts) : null,
    el("section", { class: "detail-section" }, [el("h3", { text: t("referenceNumbers") }), el("div", { class: "reference-list" }, references)]),
    el("section", { class: "detail-section" }, [el("h3", { text: t("fitments") }), el("div", { class: "fitment-list" }, cars)]),
    currentEventId && pilotMode ? feedbackPanel() : null,
  ]);

  const offerItems = item.offers || item.supplier_offers;
  const offers = el("aside", { class: "offers-panel" }, [
    el("h3", { text: t("sellers", offerItems.length) }),
    ...offerItems.map(offerNode),
    offerItems.length ? null : el("p", { class: "muted", text: t("noOffers") }),
  ]);

  detailView.replaceChildren(back, el("div", { class: "detail-shell" }, [main, offers]));
  showOnly(detailView);
}

// ---------- Suggestions while typing ----------

const suggestions = $("#suggestions");
let suggestTimer = 0;
let suggestSeq = 0;
let suggestionEntries = [];
let activeSuggestion = -1;

function closeSuggestions() {
  suggestSeq += 1; // ignore answers still on their way
  clearTimeout(suggestTimer);
  suggestions.hidden = true;
  suggestions.replaceChildren();
  suggestionEntries = [];
  activeSuggestion = -1;
  input.setAttribute("aria-expanded", "false");
  input.removeAttribute("aria-activedescendant");
}

async function loadSuggestions() {
  const query = input.value.trim();
  if (query.length < 2) {
    closeSuggestions();
    return;
  }
  const requestId = ++suggestSeq;
  try {
    const response = await fetch(`/api/v1/suggest?${carParams(new URLSearchParams({ q: query }))}`);
    if (requestId !== suggestSeq || !response.ok) return;
    renderSuggestions(await response.json());
  } catch { /* the search button still works without suggestions */ }
}

function renderSuggestions(data) {
  const groups = [];
  if (data.corrected_query) {
    groups.push([t("suggestFix"), [{ kind: "fix", label: data.corrected_query, run: () => navigate({ query: data.corrected_query, category: "" }) }]]);
  }
  if (data.part_types?.length) {
    groups.push([t("suggestTypes"), data.part_types.map((type) => ({ kind: "type", label: localName(type), meta: t("parts", type.part_count), run: () => navigate({ query: "", category: type.id }) }))]);
  }
  if (data.products?.length) {
    groups.push([t("suggestParts"), data.products.map((item) => ({ kind: "product", label: item.name, meta: item.brand?.name, run: () => openProduct(item.id) }))]);
  }
  if (!groups.length) {
    closeSuggestions();
    return;
  }
  suggestionEntries = groups.flatMap(([, entries]) => entries);
  activeSuggestion = -1;
  let position = 0;
  suggestions.replaceChildren(...groups.flatMap(([title, entries]) => [
    el("div", { class: "suggestion-group", role: "presentation", text: title }),
    ...entries.map((entry) => {
      const index = position++;
      return el("div", { id: `suggestion-${index}`, role: "option", "aria-selected": "false", class: `suggestion suggestion-${entry.kind}`, onclick: () => chooseSuggestion(index) }, [
        el("span", { class: "suggestion-label", text: entry.label }),
        entry.meta ? el("span", { class: "suggestion-meta", text: entry.meta }) : null,
      ]);
    }),
  ]));
  suggestions.hidden = false;
  input.setAttribute("aria-expanded", "true");
}

function chooseSuggestion(index) {
  const entry = suggestionEntries[index];
  closeSuggestions();
  entry.run();
}

function highlightSuggestion(index) {
  activeSuggestion = index;
  suggestions.querySelectorAll("[role=option]").forEach((node, position) => node.setAttribute("aria-selected", String(position === index)));
  if (index < 0) {
    input.removeAttribute("aria-activedescendant");
    return;
  }
  input.setAttribute("aria-activedescendant", `suggestion-${index}`);
  $(`#suggestion-${index}`).scrollIntoView({ block: "nearest" });
}

input.addEventListener("input", () => {
  clearTimeout(suggestTimer);
  suggestTimer = setTimeout(loadSuggestions, 250);
});
input.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeSuggestions(); // also cancels a list that is still on its way
    return;
  }
  if (suggestions.hidden) return;
  if (event.key === "ArrowDown" || event.key === "ArrowUp") {
    event.preventDefault();
    // Cycles through every suggestion and back to the typed text (-1).
    const slots = suggestionEntries.length + 1;
    const step = event.key === "ArrowDown" ? 1 : -1;
    highlightSuggestion(((activeSuggestion + 1 + step + slots) % slots) - 1);
  } else if (event.key === "Enter" && activeSuggestion >= 0) {
    event.preventDefault();
    chooseSuggestion(activeSuggestion);
  }
});
// Keep focus in the box while a suggestion is pressed, so the tap lands on it.
suggestions.addEventListener("mousedown", (event) => event.preventDefault());
document.addEventListener("click", (event) => {
  if (!form.contains(event.target)) closeSuggestions();
});

// ---------- Language, text size, and page wiring ----------

function renderExamples() {
  $("#example-list").replaceChildren(...t("exampleQueries").map((query) => el("button", {
    type: "button",
    class: "example",
    lang,
    text: query,
    onclick: () => navigate({ query, category: "" }),
  })));
}

function applyLanguage() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach((node) => { node.textContent = t(node.dataset.i18n); });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => { node.placeholder = t(node.dataset.i18nPlaceholder); });
  document.querySelectorAll("[data-i18n-aria]").forEach((node) => { node.setAttribute("aria-label", t(node.dataset.i18nAria)); });
  document.querySelectorAll("[data-lang]").forEach((button) => { button.setAttribute("aria-pressed", String(button.dataset.lang === lang)); });
  renderExamples();
  renderGarage();
  renderGroups();
  if (!resultsView.hidden && lastResponse) renderResults();
  if (!detailView.hidden && lastDetail) renderDetail();
}

document.querySelectorAll("[data-lang]").forEach((button) => button.addEventListener("click", () => {
  lang = button.dataset.lang;
  storage.set("megaparts_lang", lang);
  closeSuggestions();
  applyLanguage();
}));

const textSize = $("#text-size");
const setTextSize = (large) => {
  document.documentElement.classList.toggle("text-large", large);
  textSize.setAttribute("aria-pressed", String(large));
};
setTextSize(storage.get("megaparts_text_large") === "1");
textSize.addEventListener("click", () => {
  const large = !document.documentElement.classList.contains("text-large");
  setTextSize(large);
  storage.set("megaparts_text_large", large ? "1" : "0");
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  closeSuggestions();
  // A typed search looks through every section; the part-type buttons narrow it afterwards.
  if (input.value.trim()) navigate({ query: input.value, category: "" });
});

function applyUrl() {
  const params = new URLSearchParams(location.search);
  state.query = params.get("q") || "";
  state.category = params.get("cat") || "";
  state.all = params.has("all");
  state.spellcheck = true;
  input.value = state.query;
  const product = params.get("product");
  if (product) openProduct(product, false);
  else if (lastResponse && lastResponseUrl === urlFor()) renderResults();
  else if (state.query || state.category || (state.all && hasCar())) runSearch({ push: false });
  else showHome(false);
}

window.addEventListener("popstate", applyUrl);

applyLanguage();
Promise.all([
  fetch("/api/v1/vehicles").then((response) => response.json()).then((data) => { vehicles = data; }).catch(() => {}),
  loadGroups(),
]).then(async () => {
  // Forget a remembered car that is no longer in the catalog.
  if (car.make && !vehicles.some((vehicle) => vehicle.make === car.make)) {
    car = {};
    storage.set("megaparts_car", "{}");
    groupsForCar = null;
  }
  renderGarage();
  renderGroups();
  applyUrl();
});
