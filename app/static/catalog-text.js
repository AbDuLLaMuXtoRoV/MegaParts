// Catalog data in the buyer's language. The catalog is written in Uzbek; the workbook adds
// Russian and English product names, and the few free-text notes are translated by phrase.
// Text already in the buyer's language (and all Uzbek) passes through unchanged.
const CatalogText = (() => {
  const LANGS = { uz: 0, ru: 1, en: 2 };
  const pick = (lang, uz, ru, en) => [uz, ru, en][LANGS[lang] ?? 0];

  // English names are generic ("Spark plugs"); the codes in the Russian name (IRIDIUM,
  // H7 12V 55W, 880) tell parts apart without mixing in another language.
  const SPEC = /^[A-Za-z0-9][A-Za-z0-9.\-/+]*$/;
  const isSpec = (token) => SPEC.test(token) && (/\d/.test(token)
    ? /[A-Za-z]/.test(token) || token.length >= 3
    : token.length > 1 && token === token.toUpperCase());

  // Some Uzbek catalog names carry Cyrillic words ("Termostat "Дазмол"", "(bochka) (бочка)").
  const UZBEK_LATIN = {
    а: "a", б: "b", в: "v", г: "g", д: "d", е: "e", ё: "yo", ж: "j", з: "z", и: "i", й: "y",
    к: "k", л: "l", м: "m", н: "n", о: "o", п: "p", р: "r", с: "s", т: "t", у: "u", ф: "f",
    х: "x", ц: "ts", ч: "ch", ш: "sh", щ: "sh", ъ: "", ы: "i", ь: "", э: "e", ю: "yu", я: "ya",
    ў: "o‘", қ: "q", ғ: "g‘", ҳ: "h",
  };
  const CYRILLIC = /[А-Яа-яЁёЎўҚқҒғҲҳ]/g;
  const latin = (text) => text.replace(CYRILLIC, (char) => {
    const lower = char.toLowerCase();
    const out = UZBEK_LATIN[lower] ?? char;
    return char === lower ? out : out.charAt(0).toUpperCase() + out.slice(1);
  });
  function uzbekName(name) {
    if (!/[А-Яа-яЁё]/.test(name)) return name;
    const words = new Set((name.match(/[A-Za-z']+/g) || []).map((word) => word.toLowerCase()));
    // A Cyrillic repeat of a word already in the name is dropped: "(bochka) (бочка)".
    const deduped = name.replace(/\s*[("«]+([А-Яа-яЁё]+)[)"»]+/g, (match, word) => (words.has(latin(word).toLowerCase()) ? "" : match));
    return latin(deduped).replace(/\s{2,}/g, " ").trim();
  }

  // A few Russian catalog names carry Uzbek endings or typos ("(6-тали)", "Печка олди");
  // they should be fixed in the workbook too. \b does not work with Cyrillic, hence lookarounds.
  const NOT_CYRILLIC_AFTER = "(?![А-Яа-яЁё])";
  const RUSSIAN_FIXES = [
    [/(\d+)-та штеккер/g, "$1-контактный разъём"],
    [new RegExp(`(\\d+)-тишлик${NOT_CYRILLIC_AFTER}`, "g"), "$1 зубцов"],
    // The workbook does not say what "2-тали" / "6-тали" counts, so only the variant is named.
    [new RegExp(`(\\d+)-тали${NOT_CYRILLIC_AFTER}`, "g"), "вариант $1"],
    [new RegExp(`(\\d+)-контактли${NOT_CYRILLIC_AFTER}`, "g"), "$1-контактные"],
    [new RegExp(`(?<![А-Яа-яЁё])олди${NOT_CYRILLIC_AFTER}`, "g"), "передняя"],
    [/внутренная/g, "внутренняя"],
  ];
  const russianName = (name) => RUSSIAN_FIXES.reduce((text, [pattern, replacement]) => text.replace(pattern, replacement), name);

  function productName(item, lang) {
    if (lang === "ru") return item.name_ru ? russianName(item.name_ru) : uzbekName(item.name);
    if (lang !== "en" || !item.name_en) return uzbekName(item.name);
    const base = item.name_en;
    const specs = (item.name_ru || "").replace(/[(),«»"]/g, " ").split(/\s+/)
      .filter((token) => isSpec(token) && !base.toLowerCase().includes(token.toLowerCase()));
    return [base, ...new Set(specs)].join(" ");
  }

  const NO_BRAND = /^(brendsiz|no[\s-]?bre?a?nd|без бренда)/i;
  // null for the catalog's "no brand" placeholder, so the page shows its own wording.
  const brandName = (brand) => (!brand || NO_BRAND.test(brand.name) ? null : brand.name);

  const SUPPLIER_TYPES = {
    DISTRIBUTOR: ["distribyutor", "дистрибьютор", "distributor"],
    DEALER: ["diler", "дилер", "dealer"],
    WHOLESALER: ["ulgurji sotuvchi", "оптовик", "wholesaler"],
    RETAILER: ["do‘kon", "магазин", "shop"],
  };
  // "IRIZON (distribyutor)": the bracketed type word is shown in the buyer's language.
  const TYPE_SUFFIX = /\s*\((distribyutor|дистрибьютор|distributor|diler|дилер|dealer|ulgurji[^)]*|оптовик|wholesaler|do['ʻ‘’]?kon|магазин|shop)\)\s*$/i;
  function supplierName(supplier, lang) {
    const type = SUPPLIER_TYPES[supplier.supplier_type];
    if (!type) return supplier.name;
    return `${supplier.name.replace(TYPE_SUFFIX, "")} (${pick(lang, ...type)})`;
  }

  const CITIES = {
    toshkent: ["Toshkent", "Ташкент", "Tashkent"],
    samarqand: ["Samarqand", "Самарканд", "Samarkand"],
    buxoro: ["Buxoro", "Бухара", "Bukhara"],
    andijon: ["Andijon", "Андижан", "Andijan"],
    "farg'ona": ["Farg‘ona", "Фергана", "Fergana"],
    namangan: ["Namangan", "Наманган", "Namangan"],
    qarshi: ["Qarshi", "Карши", "Karshi"],
    nukus: ["Nukus", "Нукус", "Nukus"],
    urganch: ["Urganch", "Ургенч", "Urgench"],
    termiz: ["Termiz", "Термез", "Termez"],
    jizzax: ["Jizzax", "Джизак", "Jizzakh"],
    guliston: ["Guliston", "Гулистан", "Gulistan"],
    navoiy: ["Navoiy", "Навои", "Navoi"],
  };
  const CITY_WORD = /\b(Toshkent|Samarqand|Buxoro|Andijon|Farg['ʻ‘’]?ona|Namangan|Qarshi|Nukus|Urganch|Termiz|Jizzax|Guliston|Navoiy)\b/gi;
  const placeName = (text, lang) => (text || "").replace(CITY_WORD, (word) => {
    const key = word.toLowerCase().replace(/['ʻ‘’]/, "'").replace("fargona", "farg'ona");
    return CITIES[key] ? pick(lang, ...CITIES[key]) : word;
  });

  // Fitment notes from the workbook, e.g. "Avlod ko'rsatilmagan — N100 va N150 ga yoyildi".
  const A = "['ʻ‘’`]";
  const NOTE_PHRASES = {
    ru: [
      [new RegExp(`^${A}([^'ʻ‘’\`]+)${A} deb yozilgan`), "Указано как «$1»"],
      [/([\d.]+) dvigatel (\d+)-avlodda/, "двигатель $1 — у $2-го поколения"],
      [/avlodni tekshiring/, "проверьте поколение"],
      [new RegExp(`model yili bo${A}yicha farq`), "различается по модельному году"],
      [new RegExp(`^Avlod ko${A}rsatilmagan`), "Поколение не указано"],
      [/(\S+) va (\S+) ga yoyildi/, "отнесено к $1 и $2"],
      [/^(\S+) versiya$/, "версия $1"],
      [/^KPP: AT$/, "КПП: автомат"],
      [/^KPP: MT$/, "КПП: механика"],
      [/^Komplektatsiya \(pozitsiya\)/, "Комплектация (позиция)"],
      [new RegExp(`^Ta${A}minotchi:`), "Поставщик:"],
      [/tekshiring/, "проверьте"],
    ],
    en: [
      [new RegExp(`^${A}([^'ʻ‘’\`]+)${A} deb yozilgan`), "Listed as “$1”"],
      [/([\d.]+) dvigatel (\d+)-avlodda/, "the $1 engine is from generation $2"],
      [/avlodni tekshiring/, "check the generation"],
      [new RegExp(`model yili bo${A}yicha farq`), "differs by model year"],
      [new RegExp(`^Avlod ko${A}rsatilmagan`), "Generation not specified"],
      [/(\S+) va (\S+) ga yoyildi/, "applied to $1 and $2"],
      [/^(\S+) versiya$/, "$1 version"],
      [/^KPP: AT$/, "Gearbox: automatic"],
      [/^KPP: MT$/, "Gearbox: manual"],
      [/^Komplektatsiya \(pozitsiya\)/, "Trim (position)"],
      [new RegExp(`^Ta${A}minotchi:`), "Supplier:"],
      [/tekshiring/, "check"],
    ],
  };
  const noteText = (note, lang) => (NOTE_PHRASES[lang] || [])
    .reduce((text, [pattern, replacement]) => text.replace(pattern, replacement), note || "");

  // Uzbek words inside car generation labels, e.g. "II · 1.0T (Xitoy)".
  const VEHICLE_WORDS = {
    ru: [
      [/\(model aniqlanmagan\)/i, "(модель не указана)"],
      [/Model aniqlanmagan — fitmentni aniqlang/i, "Модель не указана — уточните применимость"],
      [/\bXitoy\b/g, "Китай"],
      [/\batmosfera\b/g, "атмосферный"],
      [/\bdizel\b/g, "дизель"],
      [/\brestyle\b/g, "рестайлинг"],
    ],
    en: [
      [/\(model aniqlanmagan\)/i, "(model not specified)"],
      [/Model aniqlanmagan — fitmentni aniqlang/i, "Model not specified — confirm the fit"],
      [/\bXitoy\b/g, "China"],
      [/\batmosfera\b/g, "naturally aspirated"],
      [/\bdizel\b/g, "diesel"],
      [/\brestyle\b/g, "facelift"],
    ],
  };
  const vehicleText = (text, lang) => (VEHICLE_WORDS[lang] || [])
    .reduce((value, [pattern, replacement]) => value.replace(pattern, replacement), text || "");

  // The product's own origin field: OE/genuine or aftermarket; anything else is not shown.
  function originLabel(origin, lang) {
    const value = String(origin || "").toUpperCase();
    if (["GENUINE", "OEM", "OE", "ORIGINAL"].includes(value)) return pick(lang, "Original (GM)", "Оригинал (GM)", "Genuine (GM)");
    if (value === "AFTERMARKET") return pick(lang, "Analog", "Аналог", "Aftermarket");
    return null;
  }

  return { productName, brandName, supplierName, placeName, noteText, vehicleText, originLabel };
})();
