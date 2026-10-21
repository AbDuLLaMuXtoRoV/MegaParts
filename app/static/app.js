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
    pageTitle: "MegaParts — avtomobil ehtiyot qismlari",
    tagline: "Ehtiyot qismlar katalogi",
    heroEyebrow: "Chevrolet, Daewoo va boshqa mashinalar uchun",
    heroParts: (n) => `${n} ta detal`,
    heroModels: (n) => `${n} ta mashina modeli`,
    heroSections: (n) => `${n} ta bo‘lim`,
    value1Title: "Mosligini tekshiramiz",
    value1Text: "Har bir detalda mashinangizga mos kelishi yozilgan",
    value2Title: "Narxlarni solishtiring",
    value2Text: "Bir detal uchun turli sotuvchilar takliflari",
    value3Title: "Oldindan to‘lovsiz",
    value3Text: "Band qiling, to‘lovni olib ketayotganda qiling",
    value4Title: "Sotuvchidan so‘rang",
    value4Text: "Ishonchingiz komil bo‘lmasa, Telegram’da yozing",
    popularCarsTitle: "Mashina bo‘yicha tanlash",
    popularCarsLead: "Mashinangizni bosing — faqat unga mos detallar qoladi.",
    howTitle: "Qanday ishlaydi",
    how1Title: "Mashinangizni tanlang",
    how1Text: "Marka va modelni tanlang, xohlasangiz VIN raqamini ham kiriting.",
    how2Title: "Detalni toping",
    how2Text: "Nomini yozing yoki bo‘limdan tanlang — mos kelishini darhol ko‘rasiz.",
    how3Title: "Band qiling va olib keting",
    how3Text: "Sotuvchi tasdiqlaydi, siz detalni olib ketasiz. Oldindan to‘lov yo‘q.",
    footerAbout: "Sotuvchilarning avtomobil ehtiyot qismlari bitta katalogda: mos kelishini tekshiring, narxlarni solishtiring va band qiling.",
    footerCatalog: "Katalog",
    footerChooseCar: "Mashinani tanlash",
    footerForSellers: "Sotuvchilar uchun",
    footerStaffLogin: "Xodimlar kabineti",
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
    fitChooseCar: "Mashinangizni tanlang — mos kelishini tekshiramiz",
    fitYes: (car) => `Mashinangizga mos: ${car}`,
    fitCheck: "Mos keladi, lekin shartni tekshiring",
    fitSomeVersions: (versions) => `Faqat ba’zi versiyalarga mos: ${versions}. Avlodni tanlang.`,
    fitOtherVersions: (versions) => `Sizning versiyangiz uchun emas. Mos keladi: ${versions}`,
    fitNo: (cars) => `Mashinangiz uchun ko‘rsatilmagan. Mos keladi: ${cars}`,
    fitNoData: "Mashina ma’lumoti yo‘q — sotuvchidan so‘rang",
    whyFits: (text) => `Ro‘yxatda: ${text}`,
    fitCondition: "Shart",
    fitWarning: (car, n) => `Xaridorlar xabari: to‘g‘ri kelmadi — ${car} (${n} marta)`,
    askSeller: "Ishonchingiz komil emasmi? Sotuvchidan so‘rang",
    askSellerTelegram: "Telegram’da so‘rash",
    askSellerHint: "Mashinangiz va VIN xabarga qo‘shiladi. Eski detal rasmini ham yuboring.",
    tgMessage: (part, numbers, carText, vin) => `Assalomu alaykum! MegaParts orqali yozyapman.\nDetal: ${part}\nRaqam: ${numbers}\nMashina: ${carText}\nVIN: ${vin}\nShu detal mashinamga to‘g‘ri keladimi? Eski detal rasmini yuboraman.`,
    tgReservation: (id) => `Buyurtma №${id}`,
    notGiven: "ko‘rsatilmagan",
    myCars: "Mening mashinalarim:",
    quickCars: "Tez tanlash:",
    vinLabel: "VIN raqami (ixtiyoriy)",
    vinHint: "17 ta belgi, texpasportda yozilgan",
    vinInvalid: "VIN 17 ta belgidan iborat (I, O, Q harflarisiz)",
    vinUzbek: "O‘zbekistonda ishlab chiqarilgan (UzAuto Motors)",
    vinKorea: "Janubiy Koreyada ishlab chiqarilgan (GM Korea / Daewoo)",
    vinOther: "VIN saqlandi",
    originGENUINE: "Original (GM)",
    originOE: "Zavod yetkazuvchisi brendi",
    originAFTERMARKET: "Analog",
    originBUDGET: "Arzon variant",
    conditionNEW: "Yangi",
    conditionUSED: "Ishlatilgan",
    conditionREMANUFACTURED: "Qayta tiklangan",
    warranty: (n) => `${n} oy kafolat`,
    returns: (n) => `${n} kun ichida qaytarish`,
    inStockNow: "Hozir bor",
    toOrder: (n) => `Buyurtma: ${n} kunda`,
    outdated: (d) => `Narx eskirgan bo‘lishi mumkin (${d} kun oldin yangilangan)`,
    verifiedSeller: "Tekshirilgan sotuvchi",
    unverifiedSeller: "Hujjatlari hali tekshirilmagan",
    reliability: (p, n) => `Ishonchlilik: ${p}% (${n} ta buyurtma)`,
    newSeller: "Yangi sotuvchi",
    memberSince: (year) => `${year} yildan MegaParts’da`,
    hours: "Ish vaqti",
    showMap: "Xaritada ko‘rish",
    reserveCar: "Mashina",
    reserveNote: "Izoh (ixtiyoriy)",
    reserveNoteHint: "Masalan: old chap tomoni kerak",
    reserveSentNumber: (id) => `So‘rov №${id} yuborildi. Holatini “Buyurtmalarim” bo‘limida kuzating.`,
    messageSeller: "Sotuvchiga Telegram’da yozish",
    myReservations: "Buyurtmalarim",
    noReservations: "Hali buyurtma yo‘q. Detal sahifasida “Band qilish” tugmasini bosing.",
    statusREQUESTED: "Yuborildi — sotuvchi javobini kuting",
    statusCONFIRMED: "Sotuvchi tasdiqladi",
    statusREADY: "Olib ketishga tayyor",
    statusCOMPLETED: "Yakunlandi",
    statusCANCELLED: "Bekor qilindi",
    quantityShort: (n) => `${n} dona`,
    alternativesTitle: "Muqobil variantlar",
    sameNumber: (number) => `Xuddi shu raqam (${number}), boshqa brend`,
    sameType: "Shu mashina uchun boshqa variant",
    completeJobTitle: "Odatda birga almashtiriladi",
    offerCount: (n) => `${n} ta taklif`,
    oftenReserved: "Ko‘p band qilinadi",
    fitQuestion: (car) => `Bu detal mashinangizga (${car}) to‘g‘ri keldimi?`,
    fitThanks: "Rahmat! Bu boshqa xaridorlarga yordam beradi.",
    requestTitle: "Topa olmadingizmi? Sotuvchilardan so‘rang",
    requestText: "Nima kerakligini yozing — sotuvchilar topib, siz bilan bog‘lanishadi.",
    requestWhat: "Qanday detal kerak?",
    requestContact: "Telefon yoki Telegram",
    requestSend: "So‘rov yuborish",
    requestSent: "So‘rov yuborildi. Tez orada bog‘lanamiz.",
    requestOpen: "Kerakli detal yo‘qmi? So‘rov qoldiring",
  },
  ru: {
    skipToContent: "Перейти к содержанию",
    pageTitle: "MegaParts — автозапчасти",
    tagline: "Каталог автозапчастей",
    heroEyebrow: "Для Chevrolet, Daewoo и других машин",
    heroParts: (n) => `${n} ${ruPlural(n, "деталь", "детали", "деталей")}`,
    heroModels: (n) => `${n} ${ruPlural(n, "модель", "модели", "моделей")} машин`,
    heroSections: (n) => `${n} ${ruPlural(n, "раздел", "раздела", "разделов")}`,
    value1Title: "Проверяем совместимость",
    value1Text: "У каждой детали указано, подходит ли она к вашей машине",
    value2Title: "Сравнивайте цены",
    value2Text: "Предложения разных продавцов на одну деталь",
    value3Title: "Без предоплаты",
    value3Text: "Бронируйте сейчас, платите при получении",
    value4Title: "Спросите продавца",
    value4Text: "Не уверены — напишите в Telegram",
    popularCarsTitle: "Выбор по машине",
    popularCarsLead: "Нажмите на свою машину — останутся только подходящие детали.",
    howTitle: "Как это работает",
    how1Title: "Выберите машину",
    how1Text: "Укажите марку и модель, при желании — VIN-номер.",
    how2Title: "Найдите деталь",
    how2Text: "Напишите название или выберите раздел — сразу видно, подходит ли она.",
    how3Title: "Забронируйте и заберите",
    how3Text: "Продавец подтверждает, вы забираете деталь. Без предоплаты.",
    footerAbout: "Автозапчасти от продавцов в одном каталоге: проверьте совместимость, сравните цены и забронируйте.",
    footerCatalog: "Каталог",
    footerChooseCar: "Выбрать машину",
    footerForSellers: "Для продавцов",
    footerStaffLogin: "Вход для сотрудников",
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
    fitChooseCar: "Выберите машину — проверим, подходит ли деталь",
    fitYes: (car) => `Подходит для вашей машины: ${car}`,
    fitCheck: "Подходит, но проверьте условие",
    fitSomeVersions: (versions) => `Подходит только некоторым версиям: ${versions}. Выберите поколение.`,
    fitOtherVersions: (versions) => `Не для вашей версии. Подходит: ${versions}`,
    fitNo: (cars) => `Не указана для вашей машины. Подходит: ${cars}`,
    fitNoData: "Нет данных о машинах — уточните у продавца",
    whyFits: (text) => `В списке: ${text}`,
    fitCondition: "Условие",
    fitWarning: (car, n) => `Покупатели сообщили, что не подошло к ${car} (${n} раз)`,
    askSeller: "Не уверены? Спросите продавца",
    askSellerTelegram: "Спросить в Telegram",
    askSellerHint: "Машина и VIN добавятся в сообщение. Пришлите и фото старой детали.",
    tgMessage: (part, numbers, carText, vin) => `Здравствуйте! Пишу через MegaParts.\nДеталь: ${part}\nНомер: ${numbers}\nМашина: ${carText}\nVIN: ${vin}\nПодойдёт ли эта деталь к моей машине? Пришлю фото старой детали.`,
    tgReservation: (id) => `Заявка №${id}`,
    notGiven: "не указан",
    myCars: "Мои машины:",
    quickCars: "Быстрый выбор:",
    vinLabel: "VIN-номер (необязательно)",
    vinHint: "17 символов, указан в техпаспорте",
    vinInvalid: "VIN — 17 символов, без букв I, O и Q",
    vinUzbek: "Собрана в Узбекистане (UzAuto Motors)",
    vinKorea: "Собрана в Южной Корее (GM Korea / Daewoo)",
    vinOther: "VIN сохранён",
    originGENUINE: "Оригинал (GM)",
    originOE: "Бренд заводского поставщика",
    originAFTERMARKET: "Аналог",
    originBUDGET: "Бюджетный",
    conditionNEW: "Новая",
    conditionUSED: "Б/у",
    conditionREMANUFACTURED: "Восстановленная",
    warranty: (n) => `Гарантия ${n} мес.`,
    returns: (n) => `Возврат ${n} дн.`,
    inStockNow: "В наличии сейчас",
    toOrder: (n) => `Под заказ: ${n} дн.`,
    outdated: (d) => `Цена могла устареть (обновлено ${d} дн. назад)`,
    verifiedSeller: "Проверенный продавец",
    unverifiedSeller: "Документы ещё не проверены",
    reliability: (p, n) => `Надёжность: ${p}% (${n} ${ruPlural(n, "заказ", "заказа", "заказов")})`,
    newSeller: "Новый продавец",
    memberSince: (year) => `На MegaParts с ${year} г.`,
    hours: "Часы работы",
    showMap: "На карте",
    reserveCar: "Машина",
    reserveNote: "Комментарий (необязательно)",
    reserveNoteHint: "Например: нужна передняя левая",
    reserveSentNumber: (id) => `Заявка №${id} отправлена. Статус — в разделе «Мои заказы».`,
    messageSeller: "Написать продавцу в Telegram",
    myReservations: "Мои заказы",
    noReservations: "Заказов пока нет. Нажмите «Забронировать» на странице детали.",
    statusREQUESTED: "Отправлена — ждём ответа продавца",
    statusCONFIRMED: "Продавец подтвердил",
    statusREADY: "Готов к выдаче",
    statusCOMPLETED: "Выполнен",
    statusCANCELLED: "Отменён",
    quantityShort: (n) => `${n} шт.`,
    alternativesTitle: "Альтернативы",
    sameNumber: (number) => `Тот же номер (${number}), другой бренд`,
    sameType: "Другой вариант для этой машины",
    completeJobTitle: "Обычно меняют вместе",
    offerCount: (n) => `${n} ${ruPlural(n, "предложение", "предложения", "предложений")}`,
    oftenReserved: "Часто бронируют",
    fitQuestion: (car) => `Подошла ли эта деталь к вашей машине (${car})?`,
    fitThanks: "Спасибо! Это поможет другим покупателям.",
    requestTitle: "Не нашли? Спросите продавцов",
    requestText: "Напишите, что нужно — продавцы найдут деталь и свяжутся с вами.",
    requestWhat: "Какая деталь нужна?",
    requestContact: "Телефон или Telegram",
    requestSend: "Отправить запрос",
    requestSent: "Запрос отправлен. Скоро свяжемся.",
    requestOpen: "Нет нужной детали? Оставьте запрос",
  },
  en: {
    skipToContent: "Skip to main content",
    pageTitle: "MegaParts — car parts",
    tagline: "Car parts catalog",
    heroEyebrow: "For Chevrolet, Daewoo and other cars",
    heroParts: (n) => `${n} ${n === 1 ? "part" : "parts"}`,
    heroModels: (n) => `${n} car ${n === 1 ? "model" : "models"}`,
    heroSections: (n) => `${n} ${n === 1 ? "section" : "sections"}`,
    value1Title: "Fit checked",
    value1Text: "Every part says whether it fits your car",
    value2Title: "Compare prices",
    value2Text: "Offers from different sellers for one part",
    value3Title: "No prepayment",
    value3Text: "Reserve now, pay when you pick it up",
    value4Title: "Ask the seller",
    value4Text: "Not sure? Message them on Telegram",
    popularCarsTitle: "Shop by car",
    popularCarsLead: "Tap your car — only the parts that fit it will remain.",
    howTitle: "How it works",
    how1Title: "Choose your car",
    how1Text: "Pick the make and model, and add the VIN if you like.",
    how2Title: "Find the part",
    how2Text: "Type its name or pick a section — you see right away if it fits.",
    how3Title: "Reserve and pick up",
    how3Text: "The seller confirms and you collect the part. No prepayment.",
    footerAbout: "Car parts from sellers in one catalog: check the fit, compare prices and reserve.",
    footerCatalog: "Catalog",
    footerChooseCar: "Choose your car",
    footerForSellers: "For sellers",
    footerStaffLogin: "Staff sign-in",
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
    fitChooseCar: "Choose your car to check the fit",
    fitYes: (car) => `Fits your ${car}`,
    fitCheck: "Fits — check this condition",
    fitSomeVersions: (versions) => `Fits only some versions: ${versions}. Choose your generation.`,
    fitOtherVersions: (versions) => `Not for your version. Fits: ${versions}`,
    fitNo: (cars) => `Not listed for your car. Fits: ${cars}`,
    fitNoData: "No car data — ask the seller",
    whyFits: (text) => `Listed for: ${text}`,
    fitCondition: "Condition",
    fitWarning: (car, n) => `Buyers reported it did not fit a ${car} (${n} times)`,
    askSeller: "Not sure? Ask the seller",
    askSellerTelegram: "Ask on Telegram",
    askSellerHint: "Your car and VIN are added to the message. Send a photo of the old part too.",
    tgMessage: (part, numbers, carText, vin) => `Hello! Writing via MegaParts.\nPart: ${part}\nNumber: ${numbers}\nCar: ${carText}\nVIN: ${vin}\nWill this part fit my car? I can send a photo of the old part.`,
    tgReservation: (id) => `Reservation #${id}`,
    notGiven: "not given",
    myCars: "My cars:",
    quickCars: "Quick pick:",
    vinLabel: "VIN (optional)",
    vinHint: "17 characters, on your registration card",
    vinInvalid: "A VIN has 17 characters, without the letters I, O and Q",
    vinUzbek: "Built in Uzbekistan (UzAuto Motors)",
    vinKorea: "Built in South Korea (GM Korea / Daewoo)",
    vinOther: "VIN saved",
    originGENUINE: "Genuine (GM)",
    originOE: "OE supplier brand",
    originAFTERMARKET: "Aftermarket",
    originBUDGET: "Budget",
    conditionNEW: "New",
    conditionUSED: "Used",
    conditionREMANUFACTURED: "Remanufactured",
    warranty: (n) => `${n}-month warranty`,
    returns: (n) => `${n}-day returns`,
    inStockNow: "In stock now",
    toOrder: (n) => `To order: ${n} days`,
    outdated: (d) => `Price may be outdated (updated ${d} days ago)`,
    verifiedSeller: "Verified seller",
    unverifiedSeller: "Documents not checked yet",
    reliability: (p, n) => `Reliability: ${p}% (${n} ${n === 1 ? "order" : "orders"})`,
    newSeller: "New seller",
    memberSince: (year) => `On MegaParts since ${year}`,
    hours: "Hours",
    showMap: "Show on map",
    reserveCar: "Car",
    reserveNote: "Note (optional)",
    reserveNoteHint: "For example: front left side",
    reserveSentNumber: (id) => `Request #${id} sent. Follow its status under “My reservations”.`,
    messageSeller: "Message the seller on Telegram",
    myReservations: "My reservations",
    noReservations: "No reservations yet. Press “Reserve” on a part page.",
    statusREQUESTED: "Sent — waiting for the seller",
    statusCONFIRMED: "Confirmed by the seller",
    statusREADY: "Ready for pickup",
    statusCOMPLETED: "Completed",
    statusCANCELLED: "Cancelled",
    quantityShort: (n) => `Qty ${n}`,
    alternativesTitle: "Alternatives",
    sameNumber: (number) => `Same number (${number}), other brand`,
    sameType: "Another option for this car",
    completeJobTitle: "Usually replaced together",
    offerCount: (n) => `${n} ${n === 1 ? "offer" : "offers"}`,
    oftenReserved: "Often reserved",
    fitQuestion: (car) => `Did this part fit your ${car}?`,
    fitThanks: "Thank you! This helps other buyers.",
    requestTitle: "Can’t find it? Ask the sellers",
    requestText: "Tell us what you need — sellers will find it and contact you.",
    requestWhat: "What part do you need?",
    requestContact: "Phone or Telegram",
    requestSend: "Send request",
    requestSent: "Request sent. We will contact you soon.",
    requestOpen: "Part not listed? Send a request",
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
// Catalog data (names, notes, car labels) in the chosen language; see catalog-text.js.
const productName = (item) => CatalogText.productName(item, lang);
const brandLabel = (brand) => CatalogText.brandName(brand) || t("noBrand");
const supplierLabel = (supplier) => CatalogText.supplierName(supplier, lang);
const noteLabel = (note) => CatalogText.noteText(note, lang);
const vehicleLabel = (text) => CatalogText.vehicleText(text, lang);

// Soft hyphens after a vowel let long words ("Электрооборудование") break at a syllable with
// a visible hyphen; browsers without a hyphenation dictionary would split them anywhere.
const SOFT_HYPHEN = String.fromCharCode(173);
const VOWEL = /[aeiouаеёиоуыэюя]/i;
const NO_BREAK_BEFORE = /[aeiouаеёиоуыэюяьъй]/i;
const hyphenate = (text) => text.replace(/\p{L}{12,}/gu, (word) => [...word].map((char, index) => (
  index >= 2 && word.length - index > 3 && VOWEL.test(char) && !NO_BREAK_BEFORE.test(word[index + 1]) ? `${char}${SOFT_HYPHEN}` : char
)).join(""));

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
const reservationsView = $("#reservations-view");
const garageList = $("#garage-list");
const quickCars = $("#quick-cars");
const vinRow = $("#vin-row");
const vinInput = $("#car-vin");
const vinStatus = $("#vin-status");

const PAGE_SIZE = 100;
// Reservations in 90 days before a part is marked "often reserved".
const POPULAR_AFTER = 3;
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

const readStored = (key, fallback) => {
  try { return JSON.parse(storage.get(key)) || fallback; } catch { return fallback; }
};
let car = readStored("megaparts_car", {});
// Cars the buyer has chosen before, so switching between family cars is one tap.
const MAX_GARAGE = 5;
let garage = readStored("megaparts_garage", []);
if (car.make && !garage.length) garage = [car];
const sameCar = (a, b) => a.make === b.make && (a.model || "") === (b.model || "") && (a.vehicle_id || "") === (b.vehicle_id || "");
const hasCar = () => Boolean(car.make);
const carLabelOf = (entry) => {
  if (entry.vehicle_id) {
    const vehicle = vehicles.find((candidate) => candidate.id === entry.vehicle_id);
    if (vehicle) return vehicleLabel([vehicle.make, vehicle.model, vehicle.generation].filter(Boolean).join(" "));
  }
  return [entry.make, entry.model].filter(Boolean).join(" ");
};
const carLabel = () => carLabelOf(car);
const VIN_PATTERN = /^[A-HJ-NPR-Z0-9]{17}$/;
// The first three characters name the factory; Uzbek-built GM cars start with XWB.
const vinMaker = (vin) => (vin.startsWith("XWB") ? t("vinUzbek") : vin.startsWith("KL") ? t("vinKorea") : t("vinOther"));
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
    tile.querySelector(".group-name").textContent = hyphenate(localName(group));
    tile.querySelector(".group-count").textContent = count ? t("parts", count) : totals.get(group.id) ? t("noneForCar") : t("comingSoon");
    return tile;
  }));
  renderHeroStats();
  renderPopularCars();
}

// The catalog's real size, counted from what is loaded.
function renderHeroStats() {
  const parts = groupsAll.reduce((sum, group) => sum + group.part_count, 0);
  const models = new Set(vehicles.map((vehicle) => `${vehicle.make}|${vehicle.model}`)).size;
  const sections = groupsAll.filter((group) => group.part_count).length;
  const stats = [[parts, "heroParts"], [models, "heroModels"], [sections, "heroSections"]].filter(([count]) => count);
  $("#hero-stats").replaceChildren(...stats.map(([count, key]) => el("li", {}, [
    el("strong", { text: formatNumber(count) }),
    ` ${t(key, count).replace(/^\S+\s/, "")}`,
  ])));
}

const CAR_ICON = '<svg viewBox="0 0 48 24" aria-hidden="true"><path d="M3 17.5v-4.2l5-1.3 5.5-5.5h15.5l7 5.5 7.5 1.4 1.5 4.1"/><circle cx="13" cy="18" r="3.2"/><circle cx="36" cy="18" r="3.2"/><path d="M16.5 18h16M13 12h23"/></svg>';

// "Shop by car": the most common models, one tap to choose.
function renderPopularCars() {
  const holder = $("#popular-cars");
  const totals = new Map();
  vehicles.forEach((vehicle) => {
    const key = `${vehicle.make}|${vehicle.model}`;
    totals.set(key, (totals.get(key) || 0) + vehicle.part_count);
  });
  const top = [...totals.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  holder.closest(".home-section").hidden = !top.length;
  holder.replaceChildren(...top.map(([key]) => {
    const [make, model] = key.split("|");
    const active = car.make === make && car.model === model;
    const choose = async () => {
      await setCar({ make, model });
      $("#sections-title").scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
    };
    const tile = el("button", { type: "button", class: `car-card${active ? " is-active" : ""}`, "aria-pressed": String(active), onclick: choose });
    tile.innerHTML = '<span class="car-card-icon"></span><span class="car-card-make"></span><span class="car-card-model"></span>';
    tile.querySelector(".car-card-icon").innerHTML = CAR_ICON;
    tile.querySelector(".car-card-make").textContent = make;
    tile.querySelector(".car-card-model").textContent = vehicleLabel(model);
    return tile;
  }));
}

// The part type's icon stands in for a photo until the catalog has pictures.
function partThumb(category, large = false) {
  const groupId = categoryIndex.get(category?.id)?.group.id || category?.id;
  const node = el("div", { class: `part-thumb${large ? " is-large" : ""}`, "aria-hidden": "true" });
  node.innerHTML = icon(groupId);
  return node;
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
  fillSelect(carGeneration, t("allGenerations"), generations.map((vehicle) => [vehicle.id, vehicleLabel(vehicle.generation) || "—"]), car.vehicle_id);
  carClear.hidden = !hasCar();
  renderCarHint();
  renderGarageChips();
  renderQuickCars();
  renderVin();
}

function renderGarageChips() {
  garageList.hidden = !garage.length;
  garageList.replaceChildren(
    el("span", { class: "chips-label", text: t("myCars") }),
    ...garage.map((entry) => {
      const active = sameCar(entry, car);
      return el("span", { class: `car-chip${active ? " is-active" : ""}` }, [
        el("button", { type: "button", class: "car-chip-pick", "aria-pressed": String(active), text: carLabelOf(entry), onclick: () => setCar(entry) }),
        el("button", { type: "button", class: "chip-remove", "aria-label": t("remove", carLabelOf(entry)), title: t("remove", carLabelOf(entry)), text: "✕", onclick: () => forgetCar(entry) }),
      ]);
    }),
  );
}

// One-tap tiles for the most common models, so nobody has to work through dropdowns.
function renderQuickCars() {
  quickCars.hidden = hasCar() || !vehicles.length;
  if (quickCars.hidden) return;
  const totals = new Map();
  vehicles.forEach((vehicle) => {
    const key = `${vehicle.make}|${vehicle.model}`;
    totals.set(key, (totals.get(key) || 0) + vehicle.part_count);
  });
  const top = [...totals.entries()].sort((a, b) => b[1] - a[1]).slice(0, 6);
  quickCars.replaceChildren(
    el("span", { class: "chips-label", text: t("quickCars") }),
    ...top.map(([key]) => {
      const [make, model] = key.split("|");
      return el("button", { type: "button", class: "car-tile", title: `${make} ${model}`, text: model, onclick: () => setCar({ make, model }) });
    }),
  );
}

function renderVin() {
  vinRow.hidden = !hasCar();
  if (vinRow.hidden) return;
  if (document.activeElement !== vinInput) vinInput.value = car.vin || "";
  renderVinStatus();
}

function renderVinStatus() {
  const value = vinInput.value.trim().toUpperCase();
  vinStatus.className = "vin-status";
  if (!value) {
    vinStatus.textContent = t("vinHint");
  } else if (!VIN_PATTERN.test(value)) {
    vinStatus.textContent = t("vinInvalid");
    vinStatus.classList.add("is-error");
  } else {
    vinStatus.textContent = `✓ ${vinMaker(value)}`;
    vinStatus.classList.add("is-ok");
  }
}

vinInput.addEventListener("input", renderVinStatus);
vinInput.addEventListener("change", () => {
  const value = vinInput.value.trim().toUpperCase();
  vinInput.value = value;
  if (value && !VIN_PATTERN.test(value)) return;
  const previous = car;
  car = { ...car, vin: value || undefined };
  rememberCar(car, previous);
  renderVinStatus();
});

// Refining the same car (adding a model or generation) updates its entry; another car is added.
function rememberCar(next, previous) {
  const refines = previous && previous.make === next.make
    && (!previous.model || !next.model || previous.model === next.model);
  garage = garage.filter((entry) => !sameCar(entry, next) && !(refines && sameCar(entry, previous)));
  garage = [next, ...garage].slice(0, MAX_GARAGE);
  storage.set("megaparts_garage", JSON.stringify(garage));
  storage.set("megaparts_car", JSON.stringify(next));
}

function forgetCar(entry) {
  garage = garage.filter((saved) => !sameCar(saved, entry));
  storage.set("megaparts_garage", JSON.stringify(garage));
  if (sameCar(entry, car)) setCar({});
  else renderGarageChips();
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

async function setCar(next, { refining = false } = {}) {
  const previous = car;
  // A car chosen again brings back the VIN saved with it.
  const saved = next.make ? garage.find((entry) => sameCar(entry, next)) : null;
  car = saved ? { ...saved } : { ...next };
  if (car.make) rememberCar(car, refining ? previous : null);
  else storage.set("megaparts_car", "{}");
  lastResponseUrl = ""; // cached results were for the previous car
  renderGarage();
  await loadCarGroups();
  renderCarHint();
  renderGroups();
  if (!detailView.hidden && lastDetail) renderDetail();
  else if (!resultsView.hidden || !loading.hidden) navigate({ ...state, push: false });
}

carMake.addEventListener("change", () => setCar(carMake.value ? { make: carMake.value } : {}, { refining: true }));
carModel.addEventListener("change", () => setCar(carModel.value ? { make: car.make, model: carModel.value } : { make: car.make }, { refining: true }));
carGeneration.addEventListener("change", () => setCar(
  carGeneration.value ? { make: car.make, model: car.model, vehicle_id: carGeneration.value, vin: car.vin } : { make: car.make, model: car.model, vin: car.vin },
  { refining: true },
));
carClear.addEventListener("click", () => setCar({}));

// ---------- Views ----------

const showOnly = (element) => {
  if (element !== detailView) document.title = t("pageTitle");
  // The full welcome area is for the home page; other views get a compact top.
  document.body.classList.toggle("view-home", element === browseView);
  [browseView, loading, errorBox, resultsView, detailView, reservationsView].forEach((node) => { node.hidden = node !== element; });
};

// A part lives at /part/{id}, the address search engines index; the search stays in ?q=.
const urlFor = (product) => {
  const params = new URLSearchParams();
  if (state.query) params.set("q", state.query);
  if (state.category) params.set("cat", state.category);
  if (state.all && !state.query && !state.category) params.set("all", "1");
  const search = params.toString();
  const path = product ? `/part/${encodeURIComponent(product)}` : "/";
  return search ? `${path}?${search}` : path;
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
    el("span", { text: hyphenate(label) }),
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
    requestPanel(state.query || localName(lookupCategory(state.category))),
  );
}

function renderRequestPrompt(data) {
  const slot = $("#results-request");
  slot.replaceChildren();
  if (!data.total) return;
  const open = el("button", { type: "button", class: "link-button", text: t("requestOpen") });
  open.addEventListener("click", () => slot.replaceChildren(requestPanel(state.query)));
  slot.append(open);
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
    results.append(resultCard(item));
  });
  noResults.hidden = data.total > 0;
  if (!data.total) renderNoResults();
  resultsMore.hidden = data.total <= data.items.length;
  resultsMore.textContent = resultsMore.hidden ? "" : t("moreThanShown", data.items.length, data.total);
  renderRequestPrompt(data);
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

const meaningful = (value) => value && !["N/A", "NA", "NONE", "UNKNOWN"].includes(String(value).toUpperCase());
const vehicleName = (vehicle) => vehicleLabel([vehicle.make, vehicle.model, vehicle.generation].filter(Boolean).join(" "));
const modelNames = (fitments) => [...new Set(fitments.map(({ vehicle }) => vehicleLabel([vehicle.make, vehicle.model].filter(Boolean).join(" "))))];
const shortList = (names) => `${names.slice(0, 3).join(", ")}${names.length > 3 ? `, ${t("more", names.length - 3)}` : ""}`;

// The answer leading parts sites put on every part: does it fit the buyer's car, and why.
function fitVerdict(item) {
  const fitments = item.vehicle_fitments || [];
  if (item.universal) return { tone: "yes", title: t("fitsAll"), details: [] };
  if (!hasCar()) {
    return { tone: "neutral", title: fitments.length ? `${t("fits")} ${shortList(modelNames(fitments))}` : t("fitNoData"), details: [] };
  }
  if (!fitments.length) return { tone: "check", title: t("fitNoData"), details: [] };
  const sameModel = fitments.filter(({ vehicle }) => vehicle.make === car.make && (!car.model || vehicle.model === car.model));
  const matched = car.vehicle_id ? sameModel.filter(({ vehicle }) => vehicle.id === car.vehicle_id) : sameModel;
  if (!matched.length) {
    if (car.vehicle_id && sameModel.length) {
      return { tone: "no", title: t("fitOtherVersions", shortList([...new Set(sameModel.map(({ vehicle }) => vehicleName(vehicle)))])), details: [] };
    }
    return { tone: "no", title: t("fitNo", shortList(modelNames(fitments))), details: [] };
  }
  const listed = [...new Set(matched.map(({ vehicle }) => vehicleName(vehicle)))];
  const place = [...new Set(matched.flatMap((fitment) => [fitment.position, fitment.side]).filter(meaningful).map((value) => t(value) || value))];
  const details = [t("whyFits", [shortList(listed), ...place].join(" · "))];
  const notes = [...new Set(matched.map((fitment) => fitment.condition_note).filter(Boolean))];
  notes.forEach((note) => details.push(`${t("fitCondition")}: ${noteLabel(note)}`));
  const report = (item.fit_reports || []).find((entry) => (car.vehicle_id ? entry.vehicle_id === car.vehicle_id : entry.vehicle_label === carLabel()));
  const reportedMisfit = report && report.does_not_fit >= 2;
  if (reportedMisfit) details.push(`⚠ ${t("fitWarning", carLabel(), report.does_not_fit)}`);
  // Only some generations of the buyer's model are listed: the generation decides.
  if (!car.vehicle_id && car.model) {
    const generations = vehicles.filter((vehicle) => vehicle.make === car.make && vehicle.model === car.model);
    const covered = new Set(matched.map(({ vehicle }) => vehicle.id));
    if (generations.length > 1 && generations.some((vehicle) => !covered.has(vehicle.id))) {
      return { tone: "check", title: t("fitSomeVersions", shortList(listed)), details };
    }
  }
  if (notes.length || reportedMisfit) return { tone: "check", title: t("fitCheck"), details };
  return { tone: "yes", title: t("fitYes", carLabel()), details };
}

const VERDICT_ICON = { yes: "✓", check: "!", no: "✕", neutral: "i" };
function verdictNode(verdict, compact = false) {
  return el("div", { class: `fit-verdict is-${verdict.tone}${compact ? " is-compact" : ""}` }, [
    el("span", { class: "fit-icon", "aria-hidden": "true", text: VERDICT_ICON[verdict.tone] }),
    el("div", { class: "fit-text" }, [
      el("strong", { text: verdict.title }),
      ...(compact ? [] : verdict.details.map((line) => el("span", { class: "fit-detail", text: line }))),
    ]),
  ]);
}

function resultCard(item) {
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
    el("div", { class: "result-head" }, [
      partThumb(item.category),
      el("div", { class: "result-head-text" }, [
        el("div", { class: "result-topline" }, [
          el("p", { class: "result-type", text: localName(item.category) }),
          item.reservation_count >= POPULAR_AFTER ? el("span", { class: "popular-badge", text: t("oftenReserved") }) : null,
        ]),
        el("h3", { class: "result-name", text: productName(item) }),
        el("p", { class: "result-brand" }, [`${t("brand")}: `, el("strong", { text: brandLabel(item.brand) })]),
      ]),
    ]),
    place ? el("p", { class: "result-place", text: place }) : null,
    verdictNode(fitVerdict(item), true),
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
    // With the car, alternatives and job parts are the ones that fit it.
    const response = await fetch(`/api/v1/products/${encodeURIComponent(id)}?${carParams(new URLSearchParams())}`);
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

const telegramLink = (handle, text) => {
  const base = handle.startsWith("http") ? handle : `https://t.me/${handle.replace(/^@/, "")}`;
  return text ? `${base}${base.includes("?") ? "&" : "?"}text=${encodeURIComponent(text)}` : base;
};

// A ready message with the part, its numbers, the car and VIN, so the seller can check fit.
const sellerMessage = (item) => t(
  "tgMessage",
  productName(item),
  item.reference_numbers.map((ref) => ref.number).join(", ") || "—",
  hasCar() ? carLabel() : t("notGiven"),
  car.vin || t("notGiven"),
);

const field = (label, control) => el("label", { class: "field" }, [el("span", { class: "field-label", text: label }), control]);

function askSellerBox(item, offerItems) {
  const contact = offerItems.find((offer) => offer.supplier.telegram) || offerItems.find((offer) => offer.supplier.phone);
  if (!contact) return null;
  const { supplier } = contact;
  return el("div", { class: "ask-seller" }, [
    el("strong", { text: t("askSeller") }),
    el("p", { class: "muted", text: t("askSellerHint") }),
    el("div", { class: "ask-actions" }, [
      supplier.telegram ? el("a", { class: "primary-button", href: telegramLink(supplier.telegram, sellerMessage(item)), target: "_blank", rel: "noopener", text: t("askSellerTelegram"), onclick: () => recordAction("telegram_click", contact) }) : null,
      supplier.phone ? el("a", { class: "secondary-button", href: `tel:${supplier.phone}`, text: t("call"), onclick: () => recordAction("phone_click", contact) }) : null,
    ]),
  ]);
}

function relatedSection(title, items) {
  if (!items?.length) return null;
  const relationLabel = (related) => {
    if (related.relation === "SAME_NUMBER") return t("sameNumber", related.shared_number);
    if (related.relation === "SAME_TYPE") return t("sameType");
    return localName(related.category);
  };
  return el("section", { class: "detail-section" }, [
    el("h3", { text: title }),
    el("div", { class: "related-list" }, items.map((related) => el("button", { type: "button", class: "related-item", onclick: () => openProduct(related.id) }, [
      el("span", { class: "related-type", text: relationLabel(related) }),
      el("strong", { class: "related-name", text: productName(related) }),
      el("span", {
        class: "related-meta",
        text: [
          related.brand ? brandLabel(related.brand) : null,
          related.lowest_price != null ? formatPrice(related.lowest_price, related.currency) : related.offer_count ? t("offerCount", related.offer_count) : null,
        ].filter(Boolean).join(" · "),
      }),
    ]))),
  ]);
}

// "Did it fit?" from buyers catches wrong fitment data, the main cause of wrong parts.
function fitFeedback(item) {
  if (!hasCar() || item.universal) return null;
  const panel = el("section", { class: "fit-feedback" });
  const answer = async (fits) => {
    try {
      const response = await postJson(`/api/v1/products/${encodeURIComponent(item.id)}/fit-reports`, {
        session_id: pilotSessionId, fits, vehicle_id: car.vehicle_id || null, vehicle_label: carLabel(),
      });
      if (response.ok) item.fit_reports = await response.json();
    } catch { /* thanks either way */ }
    panel.replaceChildren(el("p", { class: "feedback-thanks", text: t("fitThanks") }));
  };
  panel.append(
    el("h3", { text: t("fitQuestion", carLabel()) }),
    el("div", { class: "feedback-actions" }, [
      el("button", { type: "button", text: t("yes"), onclick: () => answer(true) }),
      el("button", { type: "button", text: t("no"), onclick: () => answer(false) }),
    ]),
  );
  return panel;
}

function sellerTrust(supplier) {
  const year = supplier.member_since ? new Date(supplier.member_since).getFullYear() : null;
  const place = [...new Set([supplier.address, supplier.city].filter(Boolean).map((text) => CatalogText.placeName(text, lang)))].join(", ");
  return el("div", { class: "seller-trust" }, [
    el("span", { class: `trust-badge ${supplier.verified ? "is-verified" : "is-unverified"}`, text: supplier.verified ? `✓ ${t("verifiedSeller")}` : t("unverifiedSeller") }),
    el("span", {
      class: "trust-line",
      text: supplier.reliability_score != null ? t("reliability", Math.round(Number(supplier.reliability_score)), supplier.reliability_sample) : t("newSeller"),
    }),
    year ? el("span", { class: "trust-line", text: t("memberSince", year) }) : null,
    place ? el("span", { class: "trust-line", text: place }) : null,
    supplier.work_hours ? el("span", { class: "trust-line", text: `${t("hours")}: ${supplier.work_hours}` }) : null,
    supplier.map_url ? el("a", { class: "trust-link", href: supplier.map_url, target: "_blank", rel: "noopener", text: t("showMap") }) : null,
  ]);
}

const offerLabels = (offer) => [
  offer.part_origin && t(`origin${offer.part_origin}`),
  offer.condition && t(`condition${offer.condition}`),
  offer.warranty_months ? t("warranty", offer.warranty_months) : null,
  offer.return_days ? t("returns", offer.return_days) : null,
].filter(Boolean);

const leadTimeLabel = (offer) => {
  if (offer.lead_time_days === 0) return t("inStockNow");
  return offer.lead_time_days > 0 ? t("toOrder", offer.lead_time_days) : null;
};

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

function reserveForm(offer, toggle, item) {
  const quantity = el("input", { type: "number", min: "1", step: "1", value: "1", required: true, inputmode: "numeric" });
  const phone = el("input", { type: "tel", autocomplete: "tel" });
  // The car and VIN travel with the request so the seller can confirm the fit first.
  const vin = el("input", { maxlength: "17", autocomplete: "off", autocapitalize: "characters", spellcheck: "false", value: car.vin || "" });
  const note = el("input", { maxlength: "1000", placeholder: t("reserveNoteHint") });
  const status = el("p", { class: "reserve-status", role: "status" });
  const followUp = el("div", { class: "reserve-actions" });
  const formNode = el("form", { class: "reserve-form", hidden: true }, [
    field(t("reserveQty"), quantity),
    field(t("reservePhone"), phone),
    hasCar() ? el("p", { class: "reserve-car" }, [`${t("reserveCar")}: `, el("strong", { text: carLabel() })]) : null,
    field(t("vinLabel"), vin),
    field(t("reserveNote"), note),
    el("div", { class: "reserve-actions" }, [
      el("button", { type: "submit", class: "primary-button", text: t("send") }),
      el("button", { type: "button", class: "secondary-button", text: t("cancel"), onclick: () => { formNode.hidden = true; toggle.hidden = false; } }),
    ]),
    status,
    followUp,
  ]);
  formNode.addEventListener("submit", async (event) => {
    event.preventDefault();
    const amount = Number(quantity.value);
    if (!Number.isInteger(amount) || amount < 1) return;
    const vinValue = vin.value.trim().toUpperCase();
    if (vinValue && !VIN_PATTERN.test(vinValue)) {
      status.textContent = t("vinInvalid");
      status.className = "reserve-status is-error";
      return;
    }
    if (vinValue && hasCar() && vinValue !== car.vin) {
      const previous = car;
      car = { ...car, vin: vinValue };
      rememberCar(car, previous);
    }
    let reservation = null;
    try {
      const response = await postJson("/api/v1/reservations", {
        session_id: pilotSessionId,
        search_event_id: currentEventId,
        product_id: currentProductId,
        supplier_offer_id: offer.id,
        quantity: amount,
        phone: phone.value.trim() || null,
        vehicle_id: car.vehicle_id || null,
        vehicle_label: hasCar() ? carLabel() : null,
        vin: vinValue || null,
        note: note.value.trim() || null,
      });
      if (response.ok) reservation = await response.json();
    } catch { /* reported below */ }
    status.textContent = reservation ? t("reserveSentNumber", reservation.id) : t("reserveError");
    status.className = `reserve-status ${reservation ? "is-ok" : "is-error"}`;
    if (!reservation) return;
    formNode.querySelectorAll("input, button[type=submit]").forEach((node) => { node.disabled = true; });
    const message = `${t("tgReservation", reservation.id)}\n${sellerMessage(item)}`;
    followUp.replaceChildren(
      offer.supplier.telegram ? el("a", { class: "primary-button", href: telegramLink(offer.supplier.telegram, message), target: "_blank", rel: "noopener", text: t("messageSeller") }) : null,
      el("button", { type: "button", class: "secondary-button", text: t("myReservations"), onclick: () => showReservations() }),
    );
  });
  return formNode;
}

function offerNode(offer, item) {
  const price = offer.price === null || offer.price === undefined ? t("priceOnRequest") : formatPrice(offer.price, offer.currency);
  const stock = stockSummary([offer]);
  const leadTime = leadTimeLabel(offer);
  const labels = offerLabels(offer);
  const outdated = offer.freshness_status === "OUTDATED";
  const ageDays = offer.updated_at ? Math.round((Date.now() - new Date(offer.updated_at).getTime()) / 86400000) : 0;
  const reserveButton = el("button", { type: "button", class: "primary-button", text: t("reserve") });
  const formNode = reserveForm(offer, reserveButton, item);
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
  return el("div", { class: `offer${outdated ? " is-outdated" : ""}` }, [
    el("div", { class: "offer-supplier", text: supplierLabel(offer.supplier) }),
    sellerTrust(offer.supplier),
    el("div", { class: "offer-code", text: offer.supplier_sku || t("noSellerCode") }),
    labels.length ? el("div", { class: "offer-labels" }, labels.map((label) => el("span", { class: "offer-label", text: label }))) : null,
    el("div", { class: "offer-row" }, [
      el("span", { class: "price", text: price }),
      el("span", { class: `stock stock-${stock.tone}`, text: leadTime && stock.tone !== "in" ? leadTime : stock.text }),
    ]),
    el("div", { class: "offer-freshness", text: outdated ? t("outdated", ageDays) : freshnessLabel(offer) }),
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

  const facts = [[t("partType"), localName(item.category)], [t("position"), item.position && (t(item.position) || item.position)], [t("side"), item.side && (t(item.side) || item.side)], [t("origin"), CatalogText.originLabel(item.origin, lang)]]
    .filter(([, value]) => value)
    .map(([label, value]) => el("div", { class: "fact" }, [el("span", { text: label }), el("strong", { text: value })]));

  const references = item.reference_numbers.length
    ? item.reference_numbers.map((ref) => el("span", { class: "reference", text: ref.number }))
    : [el("p", { class: "muted", text: t("noReferences") })];

  const fitmentLine = (fitment) => {
    const place = [fitment.position, fitment.side].filter(meaningful).map((value) => t(value) || value).join(" · ");
    return el("div", { class: "fitment" }, [
      el("span", { text: vehicleLabel([fitment.vehicle.make, fitment.vehicle.model, fitment.vehicle.generation].filter(Boolean).join(" · ")) }),
      place ? el("span", { class: "fitment-note", text: place }) : null,
      fitment.condition_note ? el("span", { class: "fitment-note", text: `${t("fitCondition")}: ${noteLabel(fitment.condition_note)}` }) : null,
    ]);
  };
  const cars = item.universal
    ? [el("div", { class: "fitment is-match", text: t("fitsAll") })]
    : item.vehicle_fitments.length
      ? item.vehicle_fitments.map(fitmentLine)
      : [el("p", { class: "muted", text: t("fitsUnknown") })];

  const offerItems = item.offers || item.supplier_offers;
  const main = el("article", { class: "detail-main" }, [
    el("div", { class: "detail-head" }, [
      partThumb(item.category, true),
      el("div", {}, [
        el("div", { class: "detail-topline" }, [
          el("div", { class: "detail-brand", text: brandLabel(item.brand) }),
          item.reservation_count >= POPULAR_AFTER ? el("span", { class: "popular-badge", text: t("oftenReserved") }) : null,
        ]),
        el("h2", { text: productName(item) }),
      ]),
    ]),
    verdictNode(fitVerdict(item)),
    askSellerBox(item, offerItems),
    facts.length ? el("div", { class: "facts" }, facts) : null,
    el("section", { class: "detail-section" }, [el("h3", { text: t("referenceNumbers") }), el("div", { class: "reference-list" }, references)]),
    el("section", { class: "detail-section" }, [el("h3", { text: t("fitments") }), el("div", { class: "fitment-list" }, cars)]),
    fitFeedback(item),
    relatedSection(t("alternativesTitle"), item.alternatives),
    relatedSection(t("completeJobTitle"), item.complete_the_job),
    currentEventId && pilotMode ? feedbackPanel() : null,
  ]);

  const offers = el("aside", { class: "offers-panel" }, [
    el("h3", { text: t("sellers", offerItems.length) }),
    ...offerItems.map((offer) => offerNode(offer, item)),
    offerItems.length ? null : el("p", { class: "muted", text: t("noOffers") }),
  ]);

  detailView.replaceChildren(back, el("div", { class: "detail-shell" }, [main, offers]));
  document.title = `${productName(item)} — MegaParts`;
  showOnly(detailView);
}

// ---------- My reservations ----------

let myReservations = [];

async function showReservations(push = true) {
  if (push) history.pushState(null, "", "/?view=reservations");
  showOnly(loading);
  scrollToContent();
  try {
    const response = await fetch(`/api/v1/reservations?session_id=${encodeURIComponent(pilotSessionId)}`);
    if (!response.ok) throw new Error(t("searchUnavailable"));
    myReservations = await response.json();
    renderReservations();
  } catch (error) {
    errorBox.textContent = error.message;
    showOnly(errorBox);
  }
}

function reservationCard(reservation) {
  const { supplier } = reservation;
  const reservedProduct = { name: reservation.product_name, name_ru: reservation.product_name_ru, name_en: reservation.product_name_en };
  const message = `${t("tgReservation", reservation.id)}\n${t(
    "tgMessage",
    productName(reservedProduct),
    reservation.reference_numbers.join(", ") || "—",
    reservation.vehicle_label || t("notGiven"),
    reservation.vin || t("notGiven"),
  )}`;
  const created = new Date(reservation.created_at).toLocaleDateString(lang === "en" ? "en-GB" : `${lang}-UZ`);
  return el("article", { class: "reservation-card" }, [
    el("span", { class: `reservation-status is-${reservation.status.toLowerCase()}`, text: t(`status${reservation.status}`) || reservation.status }),
    el("h3", {}, [el("button", { type: "button", class: "link-button", text: productName(reservedProduct), onclick: () => openProduct(reservation.product_id) })]),
    el("p", { class: "muted", text: [`№${reservation.id}`, created, t("quantityShort", reservation.quantity), reservation.vehicle_label, reservation.vin].filter(Boolean).join(" · ") }),
    el("p", {}, [el("strong", { text: supplierLabel(supplier) }), reservation.price != null ? ` · ${formatPrice(reservation.price, reservation.currency)}` : ""]),
    el("div", { class: "reserve-actions" }, [
      supplier.telegram ? el("a", { class: "primary-button", href: telegramLink(supplier.telegram, message), target: "_blank", rel: "noopener", text: t("messageSeller") }) : null,
      supplier.phone ? el("a", { class: "secondary-button", href: `tel:${supplier.phone}`, text: t("call") }) : null,
    ]),
  ]);
}

function renderReservations() {
  reservationsView.replaceChildren(
    el("button", { type: "button", class: "back secondary-button", text: t("back"), onclick: () => showHome() }),
    el("h2", { class: "page-title", text: t("myReservations") }),
    myReservations.length
      ? el("div", { class: "reservation-list" }, myReservations.map(reservationCard))
      : el("p", { class: "muted", text: t("noReservations") }),
  );
  showOnly(reservationsView);
}

$("#my-reservations").addEventListener("click", () => showReservations());
$("#footer-year").textContent = `© ${new Date().getFullYear()}`;

// ---------- Part requests ----------

// A search that finds nothing ends in a request to sellers, not a dead end.
function requestPanel(query) {
  const what = el("input", { required: true, maxlength: "300", value: query || "" });
  const contact = el("input", { required: true, minlength: "3", maxlength: "200", autocomplete: "tel", inputmode: "tel" });
  const note = el("input", { maxlength: "1000" });
  const status = el("p", { class: "reserve-status", role: "status" });
  const formNode = el("form", { class: "request-form" }, [
    el("h3", { text: t("requestTitle") }),
    el("p", { class: "muted", text: t("requestText") }),
    field(t("requestWhat"), what),
    field(t("requestContact"), contact),
    field(t("reserveNote"), note),
    hasCar() ? el("p", { class: "reserve-car" }, [`${t("reserveCar")}: `, el("strong", { text: [carLabel(), car.vin].filter(Boolean).join(" · ") })]) : null,
    el("button", { type: "submit", class: "primary-button", text: t("requestSend") }),
    status,
  ]);
  formNode.addEventListener("submit", async (event) => {
    event.preventDefault();
    let ok = false;
    try {
      const response = await postJson("/api/v1/part-requests", {
        session_id: pilotSessionId,
        query: what.value.trim(),
        contact: contact.value.trim(),
        note: note.value.trim() || null,
        vehicle_id: car.vehicle_id || null,
        vehicle_label: hasCar() ? carLabel() : null,
        vin: car.vin || null,
      });
      ok = response.ok;
    } catch { /* reported below */ }
    status.textContent = ok ? t("requestSent") : t("reserveError");
    status.className = `reserve-status ${ok ? "is-ok" : "is-error"}`;
    if (ok) formNode.querySelectorAll("input, button").forEach((node) => { node.disabled = true; });
  });
  return formNode;
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
    groups.push([t("suggestParts"), data.products.map((item) => ({ kind: "product", label: productName(item), meta: item.brand ? brandLabel(item.brand) : null, run: () => openProduct(item.id) }))]);
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
  document.title = t("pageTitle");
  document.querySelectorAll("[data-i18n]").forEach((node) => { node.textContent = t(node.dataset.i18n); });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => { node.placeholder = t(node.dataset.i18nPlaceholder); });
  document.querySelectorAll("[data-i18n-aria]").forEach((node) => { node.setAttribute("aria-label", t(node.dataset.i18nAria)); });
  document.querySelectorAll("[data-lang]").forEach((button) => { button.setAttribute("aria-pressed", String(button.dataset.lang === lang)); });
  renderExamples();
  renderGarage();
  renderGroups();
  if (!resultsView.hidden && lastResponse) renderResults();
  if (!detailView.hidden && lastDetail) renderDetail();
  if (!reservationsView.hidden) renderReservations();
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
  // /part/{id}; ?product= links from before part pages had their own address still work.
  const partPath = location.pathname.match(/^\/part\/([^/]+)$/);
  const product = partPath ? decodeURIComponent(partPath[1]) : params.get("product");
  if (product) openProduct(product, false);
  else if (params.get("view") === "reservations") showReservations(false);
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
  // Forget remembered cars that are no longer in the catalog (only when the list loaded).
  const known = (entry) => vehicles.some((vehicle) => vehicle.make === entry.make);
  if (vehicles.length) {
    garage = garage.filter(known);
    storage.set("megaparts_garage", JSON.stringify(garage));
  }
  if (vehicles.length && car.make && !known(car)) {
    car = {};
    storage.set("megaparts_car", "{}");
    groupsForCar = null;
  }
  renderGarage();
  renderGroups();
  applyUrl();
});
