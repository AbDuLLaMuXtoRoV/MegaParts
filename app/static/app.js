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
    pageTitle: "MegaParts — zapchast qayerda bor: ehtiyot qismlar qidiruvi",
    tagline: "Ehtiyot qismlar katalogi",
    heroEyebrow: "Do‘konlar, servislar va ustalar uchun",
    heroParts: (n) => `${n} ta detal`,
    heroModels: (n) => `${n} ta mashina modeli`,
    heroSections: (n) => `${n} ta bo‘lim`,
    value1Title: "Raqam bo‘yicha aniq",
    value1Text: "Artikul, OEM yoki sotuvchi kodini yozing — PT43 va PT 43 bir xil",
    value2Title: "Kimda bor — bir qidiruvda",
    value2Text: "Bir nechta sotuvchining qoldig‘i, narxi va yangilangan vaqti",
    value3Title: "Mosligi ko‘rsatilgan",
    value3Text: "Mashina, oldi/orqa va chap/o‘ng aralashib ketmaydi",
    value4Title: "Sotuvchi bilan to‘g‘ridan-to‘g‘ri",
    value4Text: "Qo‘ng‘iroq, Telegram yoki band qilish — sizning shartlaringiz saqlanadi",
    popularCarsTitle: "Mashina bo‘yicha tanlash",
    popularCarsLead: "Mashinangizni bosing — faqat unga mos detallar qoladi.",
    howTitle: "Qanday ishlaydi",
    how1Title: "Raqam yoki nomni yozing",
    how1Text: "Artikul, OEM raqam, detal nomi yoki mashina — qanday bilsangiz shunday.",
    how2Title: "Kimda borligini ko‘ring",
    how2Text: "Har bir sotuvchining qoldig‘i, narxi va ma’lumot qachon yangilangani.",
    how3Title: "Sotuvchiga murojaat qiling",
    how3Text: "Qo‘ng‘iroq qiling, Telegram’da yozing yoki band qiling. Oldindan to‘lov yo‘q.",
    footerAbout: "O‘zbekistonda zapchast qayerda borligini toping: bir nechta sotuvchining takliflari bitta qidiruvda — artikul, OEM raqam, nom yoki mashina bo‘yicha.",
    footerCatalog: "Katalog",
    footerChooseCar: "Mashinani tanlash",
    footerForSellers: "Sotuvchilar uchun",
    footerStaffLogin: "Xodimlar kabineti",
    language: "Til",
    title: "Zapchast kimda borligini toping",
    subtitle: "Odatdagi sotuvchingizda yo‘q detalni artikul, OEM raqam, nom yoki mashina bo‘yicha qidiring — bir nechta sotuvchining takliflari bir joyda.",
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
    searchPlaceholder: "Artikul, OEM raqam yoki nom: 96273708, kolodka…",
    searchButton: "Qidirish",
    examples: "Masalan:",
    exampleQueries: ["96273708", "kolodka oldi nexia", "Cobalt svecha", "amortizator orqa"],
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
    sameNumberVariant: (number) => `Xuddi shu raqam (${number}), boshqa variant`,
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
    pageTitle: "MegaParts — где есть запчасть: поиск автозапчастей",
    tagline: "Каталог автозапчастей",
    heroEyebrow: "Для магазинов, сервисов и мастеров",
    heroParts: (n) => `${n} ${ruPlural(n, "деталь", "детали", "деталей")}`,
    heroModels: (n) => `${n} ${ruPlural(n, "модель", "модели", "моделей")} машин`,
    heroSections: (n) => `${n} ${ruPlural(n, "раздел", "раздела", "разделов")}`,
    value1Title: "Точно по номеру",
    value1Text: "Артикул, OEM или код продавца — PT43 и PT 43 одно и то же",
    value2Title: "У кого есть — в одном поиске",
    value2Text: "Наличие, цена и время обновления у нескольких продавцов",
    value3Title: "Применимость указана",
    value3Text: "Машина, перед/зад и лево/право не перепутаются",
    value4Title: "Напрямую с продавцом",
    value4Text: "Звонок, Telegram или бронь — ваши условия с продавцом сохраняются",
    popularCarsTitle: "Выбор по машине",
    popularCarsLead: "Нажмите на свою машину — останутся только подходящие детали.",
    howTitle: "Как это работает",
    how1Title: "Введите номер или название",
    how1Text: "Артикул, OEM-номер, название детали или машина — как вам удобнее.",
    how2Title: "Посмотрите, у кого есть",
    how2Text: "Наличие и цена у каждого продавца и когда данные обновлялись.",
    how3Title: "Свяжитесь с продавцом",
    how3Text: "Позвоните, напишите в Telegram или забронируйте. Без предоплаты.",
    footerAbout: "Найдите, у кого есть запчасть в Узбекистане: предложения нескольких продавцов в одном поиске — по артикулу, OEM-номеру, названию или машине.",
    footerCatalog: "Каталог",
    footerChooseCar: "Выбрать машину",
    footerForSellers: "Для продавцов",
    footerStaffLogin: "Вход для сотрудников",
    language: "Язык",
    title: "Найдите, у кого есть запчасть",
    subtitle: "Ищите деталь, которой нет у вашего обычного поставщика, по артикулу, OEM-номеру, названию или машине — предложения нескольких продавцов в одном месте.",
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
    searchPlaceholder: "Артикул, OEM-номер или название: 96273708, колодки…",
    searchButton: "Найти",
    examples: "Например:",
    exampleQueries: ["96273708", "колодки передние нексия", "Кобальт свеча", "амортизатор задний"],
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
    sameNumberVariant: (number) => `Тот же номер (${number}), другой вариант`,
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
    pageTitle: "MegaParts — where the part is in stock: car parts search",
    tagline: "Car parts catalog",
    heroEyebrow: "For parts shops, garages and mechanics",
    heroParts: (n) => `${n} ${n === 1 ? "part" : "parts"}`,
    heroModels: (n) => `${n} car ${n === 1 ? "model" : "models"}`,
    heroSections: (n) => `${n} ${n === 1 ? "section" : "sections"}`,
    value1Title: "Exact by number",
    value1Text: "Part number, OEM or seller code — PT43 and PT 43 are the same",
    value2Title: "Who has it — in one search",
    value2Text: "Stock, price and last update from several sellers",
    value3Title: "Fit shown",
    value3Text: "Car, front/rear and left/right are never mixed up",
    value4Title: "Straight to the seller",
    value4Text: "Call, Telegram or reserve — your own terms with the seller stay",
    popularCarsTitle: "Shop by car",
    popularCarsLead: "Tap your car — only the parts that fit it will remain.",
    howTitle: "How it works",
    how1Title: "Type a number or a name",
    how1Text: "Part number, OEM number, part name or car — whatever you know.",
    how2Title: "See who has it",
    how2Text: "Each seller’s stock and price, and when the data was last updated.",
    how3Title: "Contact the seller",
    how3Text: "Call, message on Telegram or reserve. No prepayment.",
    footerAbout: "Find who has the part in Uzbekistan: offers from several sellers in one search — by part number, OEM number, name or car.",
    footerCatalog: "Catalog",
    footerChooseCar: "Choose your car",
    footerForSellers: "For sellers",
    footerStaffLogin: "Staff sign-in",
    language: "Language",
    title: "Find who has the part",
    subtitle: "Search for the part your usual supplier doesn’t have — by part number, OEM number, name or car. Offers from several sellers in one place.",
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
    searchPlaceholder: "Part number, OEM number or name: 96273708, brake pads…",
    searchButton: "Search",
    examples: "Try:",
    exampleQueries: ["96273708", "front brake pads nexia", "Cobalt spark plug", "rear shock absorber"],
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
    sameNumberVariant: (number) => `Same number (${number}), another variant`,
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

// Basket, repair lists, quality grades, sellers and "sell on MegaParts".
Object.assign(STRINGS.uz, {
  basket: "Savat",
  addToBasket: "Savatga qo‘shish",
  inBasket: "Savatda ✓",
  basketTitle: "Savatingiz",
  basketLead: "Bir nechta sotuvchidan detallarni bir martada band qiling. Har bir sotuvchi o‘z qismini oladi, to‘lov olib ketayotganda.",
  basketEmpty: "Savat bo‘sh. Detal sahifasida “Savatga qo‘shish” tugmasini bosing yoki tayyor ta’mir ro‘yxatidan foydalaning.",
  basketSeller: (name) => `Sotuvchi: ${name}`,
  basketRemove: "Olib tashlash",
  basketQty: "Soni",
  basketTotal: "Jami",
  basketTotalNote: "Narxi ko‘rsatilmagan detallar narxini sotuvchi aytadi.",
  basketReserveAll: (n) => `Hammasini band qilish (${n})`,
  basketSent: "Band qilindi! Har bir sotuvchiga yozib qo‘ying — buyurtma raqamlari xabarda bo‘ladi.",
  basketGone: "Bu taklif endi mavjud emas",
  basketShare: "Ro‘yxatni ulashish",
  basketShareTelegram: "Telegram’da yuborish",
  basketCopy: "Havolani nusxalash",
  basketCopied: "Havola nusxalandi",
  basketShareText: (n) => `MegaParts: ${n} ta detal ro‘yxati`,
  basketClear: "Savatni tozalash",
  basketInLabel: "✓ Savatda",
  basketOpen: "Savatni ochish",
  basketRemoveFull: "Savatdan olib tashlash",
  basketRemoved: (name) => `“${name}” savatdan olib tashlandi.`,
  basketCleared: "Savat tozalandi.",
  undo: "Qaytarish",
  qtyLess: "Kamaytirish",
  qtyMore: "Ko‘paytirish",
  cancelReservation: "Bekor qilish",
  cancelConfirm: "Bu buyurtma bekor qilinsinmi?",
  cancelAllConfirm: "Savatdagi barcha buyurtmalar bekor qilinsinmi?",
  cancelYes: "Ha, bekor qilish",
  cancelNo: "Yo‘q",
  cancelAll: (n) => `Hammasini bekor qilish (${n})`,
  cancelled: "Bekor qilindi. Sotuvchiga ham xabar bering.",
  cancelError: "Bekor qilib bo‘lmadi. Sahifani yangilab, qayta urinib ko‘ring.",
  tellSeller: "Sotuvchiga xabar berish",
  tgCancel: (ids) => `Assalomu alaykum! MegaParts orqali qilingan buyurtma ${ids} bekor qilindi. Uzr.`,
  partNumber: "Raqam",
  refTypeOE: "OEM (zavod raqami)",
  refTypeOES: "Zavod yetkazuvchisi",
  refTypeAFTERMARKET: "Ishlab chiqaruvchi artikuli",
  refTypeSUPPLIER_SKU: "Sotuvchi kodi",
  refTypeEAN: "Shtrix-kod (EAN)",
  viewCards: "Kartochkalar",
  viewTable: "Jadval",
  colNumber: "Raqam",
  oemLabel: "OEM kodi",
  oemColumn: "OEM",
  oemUnknown: "hali aniqlanmagan",
  oemHelp: "Avtomobil zavodining shu detal uchun raqami. Shu raqam bo‘yicha aynan to‘g‘ri detalni topasiz.",
  oemCopy: "Nusxa olish",
  oemCopied: "Nusxa olindi",
  oemAsk: "OEM kodini bilasizmi? Bizga yuboring",
  oemPlaceholder: "Masalan: 96273708",
  oemSend: "Yuborish",
  oemThanks: "Rahmat! Mutaxassisimiz kodni tekshirib, saytga qo‘shadi.",
  oemInvalid: "Bu OEM kodiga o‘xshamaydi: kamida 5 ta belgi va 3 ta raqam bo‘lishi kerak.",
  oemSendError: "Yuborilmadi. Birozdan keyin qayta urinib ko‘ring.",
  oemMore: (count) => `yana ${count} ta`,
  faqLead: "Xaridorlar eng ko‘p so‘raydigan savollar.",
  sellerLabel: (n) => (n > 1 ? "Sotuvchilar" : "Sotuvchi"),
  pickerSearch: "Qidirish…",
  pickerEmpty: "Topilmadi",
  pickerPopular: "Ko‘p tanlanadi",
  pickerAll: "Barchasi",
  navLabel: "Sahifada",
  navNumbers: "Raqamlar",
  navCars: "Mashinalar",
  navAlternatives: "Muqobillar",
  navTogether: "Birga oling",
  seeSellers: (n) => `Sotuvchilarni ko‘rish (${n})`,
  colPart: "Detal",
  colFit: "Mosligi",
  colSellers: "Sotuvchilar",
  colPrice: "Narx",
  colStock: "Qoldiq",
  attr_repair_size: "Ta’mir o‘lchami",
  attr_placement: "Tashqi / ichki",
  attr_transmission: "Uzatmalar qutisi",
  attr_engine_type: "Dvigatel",
  attr_spec_code: "O‘lcham / kod",
  val_OUTER: "Tashqi",
  val_INNER: "Ichki",
  val_AT: "Avtomat (AKPP)",
  val_MT: "Mexanika (MKPP)",
  steps: ["Yuborildi", "Tasdiqlandi", "Tayyor", "Olindi"],
  basketGroup: (n) => `Savatdan ${n} ta detal`,
  basketButton: (n) => (n ? `Savat (${n})` : "Savat"),
  sharedListTitle: "Sizga yuborilgan detallar ro‘yxati",
  sharedListAdd: "Hammasini savatimga qo‘shish",
  tgBasket: (lines, carText, vin) => `Assalomu alaykum! MegaParts orqali band qildim:\n${lines}\nMashina: ${carText}\nVIN: ${vin}\nTayyor bo‘lganda xabar bering.`,
  promoNEW_ARRIVAL: "Yangi keldi",
  promoDISCOUNT: (p) => (p ? `Aksiya −${p}%` : "Aksiya"),
  promoPRICE_DROP: "Narxi tushdi",
  promoNEW_PRICE: "Yangi narx",
  warrantyKm: (months, km) => `Kafolat: ${[months ? `${months} oy` : null, km ? `${formatNumber(km)} km` : null].filter(Boolean).join(" yoki ")}`,
  listDate: (date) => `Sotuvchi ro‘yxati: ${date}`,
  favSeller: "☆ Sevimli sotuvchi qilish",
  favSellerOn: "★ Sevimli sotuvchingiz",
  qualityORIGINAL: "Original (GM)",
  qualityKOREA: "Koreya / zavod sifati",
  qualityCHINA: "Xitoy",
  qualityBUDGET: "Arzon variant",
  qualityOTHER: "Boshqa",
  qualityTitle: "Sifat bo‘yicha tanlang",
  qualityLead: "Bir xil detal raqami — turli sifat va narx.",
  tierBest: "Eng ishonchli",
  tierBetter: "Narx va sifat",
  tierGood: "Tejamkor",
  thisPart: "Shu detal",
  filterQuality: "Sifat",
  filterBrand: "Brend",
  sortLabel: "Tartib",
  sortRelevance: "Mosligi bo‘yicha",
  sortPrice: "Avval arzonlari",
  jobsTitle: "Tayyor ta’mir ro‘yxatlari",
  jobsLead: "Ta’mirni tanlang — kerakli detallarni mashinangiz uchun bir joyda ko‘rsatamiz.",
  jobSteps: (n) => `${n} ta detal`,
  jobChooseCar: "Avval mashinangizni tanlang — ro‘yxat unga moslanadi.",
  jobAddAll: (n) => `Hammasini savatga (${n})`,
  jobNone: "Hozircha sotuvda yo‘q",
  jobMore: (n) => `Boshqa variantlar (${n})`,
  jobForCar: (carText) => `${carText} uchun`,
  jobAdded: "Savatga qo‘shildi",
  sellersTitle: "Sotuvchilar",
  sellersLead: "MegaParts’dagi sotuvchilar, ularning kontaktlari va sotadigan brendlari.",
  sellerParts: (n) => `${formatNumber(n)} ta detal`,
  sellerPriced: (n) => `${formatNumber(n)} tasi narx bilan`,
  sellerOpen: "Sotuvchi sahifasi",
  sellerLastList: (date) => `Oxirgi ro‘yxat: ${date}`,
  sellTitle: "MegaParts’da soting",
  sellLead: "Ehtiyot qismlar do‘koningiz bormi? Ariza qoldiring — narxlar ro‘yxatingizni (Excel) qabul qilib, 24 soat ichida joylaymiz. Joylash bepul.",
  sellPoints: [
    "Xaridorlar detallaringizni mashinasi bo‘yicha topadi",
    "Buyurtmalar telefon va Telegram orqali keladi, oldindan to‘lovsiz",
    "Excel ro‘yxatingiz istalgan ko‘rinishda bo‘lishi mumkin — o‘zimiz tartiblaymiz",
  ],
  sellBusiness: "Do‘kon nomi",
  sellContact: "Ismingiz",
  sellPhone: "Telefon",
  sellTelegram: "Telegram (ixtiyoriy)",
  sellCity: "Shahar",
  sellAddress: "Manzil (bozor, rasta)",
  sellCars: "Qaysi mashinalar uchun detal sotasiz?",
  sellNote: "Izoh (ixtiyoriy)",
  sellSend: "Ariza yuborish",
  sellSent: "Rahmat! Tez orada siz bilan bog‘lanamiz.",
  sellBannerTitle: "Siz sotuvchimisiz?",
  sellBannerText: "Detallaringizni MegaParts’ga bepul joylang — xaridorlar sizni mashinasi bo‘yicha topadi.",
  sellBannerButton: "Batafsil",
  footerSell: "MegaParts’da sotish",
  footerSellers: "Barcha sotuvchilar",
  footerJobs: "Tayyor ta’mir ro‘yxatlari",
  faqTitle: "Ko‘p so‘raladigan savollar",
  faq: [
    ["To‘lovni qachon qilaman?", "Oldindan to‘lov yo‘q. Detalni band qilasiz, sotuvchi tasdiqlaydi, to‘lovni detalni olayotganda sotuvchiga qilasiz."],
    ["Detal mashinamga to‘g‘ri kelishini qanday bilaman?", "Mashinangizni tanlang — har bir detalda “Mos keladi” yoki “Tekshiring” belgisi chiqadi. Ikkilansangiz, “Telegram’da so‘rash” tugmasi bilan sotuvchiga mashina va VIN raqamini yuboring."],
    ["Bir nechta sotuvchidan bir martada olsam bo‘ladimi?", "Ha. Detallarni savatga qo‘shing va “Hammasini band qilish”ni bosing — har bir sotuvchi o‘z qismini oladi."],
    ["“Original”, “Koreya” va “Xitoy” nimani anglatadi?", "Original — avtozavodning o‘z detali (GM). Koreya / zavod sifati — Koreyada yoki zavod yetkazuvchisi ishlab chiqargan. Xitoy — arzonroq analog. Bir xil raqamdagi detallarni detal sahifasida solishtirasiz."],
    ["Kerakli detal topilmasa-chi?", "Qidiruv natijasi ostidagi so‘rovni to‘ldiring — sotuvchilar topib, siz bilan bog‘lanishadi."],
  ],
});
Object.assign(STRINGS.ru, {
  basket: "Корзина",
  addToBasket: "В корзину",
  inBasket: "В корзине ✓",
  basketTitle: "Ваша корзина",
  basketLead: "Забронируйте детали у нескольких продавцов за один раз. Каждый продавец получает свою часть, оплата при получении.",
  basketEmpty: "Корзина пуста. Нажмите «В корзину» на странице детали или воспользуйтесь готовым списком для ремонта.",
  basketSeller: (name) => `Продавец: ${name}`,
  basketRemove: "Убрать",
  basketQty: "Кол-во",
  basketTotal: "Итого",
  basketTotalNote: "Цену деталей без цены сообщит продавец.",
  basketReserveAll: (n) => `Забронировать всё (${n})`,
  basketSent: "Забронировано! Напишите каждому продавцу — номера заказов уже в сообщении.",
  basketGone: "Это предложение больше недоступно",
  basketShare: "Поделиться списком",
  basketShareTelegram: "Отправить в Telegram",
  basketCopy: "Скопировать ссылку",
  basketCopied: "Ссылка скопирована",
  basketShareText: (n) => `MegaParts: список из ${n} ${ruPlural(n, "детали", "деталей", "деталей")}`,
  basketClear: "Очистить корзину",
  basketInLabel: "✓ В корзине",
  basketOpen: "Открыть корзину",
  basketRemoveFull: "Убрать из корзины",
  basketRemoved: (name) => `«${name}» убрана из корзины.`,
  basketCleared: "Корзина очищена.",
  undo: "Вернуть",
  qtyLess: "Меньше",
  qtyMore: "Больше",
  cancelReservation: "Отменить",
  cancelConfirm: "Отменить этот заказ?",
  cancelAllConfirm: "Отменить все заказы из этой корзины?",
  cancelYes: "Да, отменить",
  cancelNo: "Нет",
  cancelAll: (n) => `Отменить все (${n})`,
  cancelled: "Отменено. Сообщите и продавцу.",
  cancelError: "Не удалось отменить. Обновите страницу и попробуйте снова.",
  tellSeller: "Сообщить продавцу",
  tgCancel: (ids) => `Здравствуйте! Заказ ${ids}, сделанный через MegaParts, отменён. Извините.`,
  partNumber: "Номер",
  refTypeOE: "OEM (номер завода)",
  refTypeOES: "Поставщик завода",
  refTypeAFTERMARKET: "Артикул производителя",
  refTypeSUPPLIER_SKU: "Код продавца",
  refTypeEAN: "Штрихкод (EAN)",
  viewCards: "Карточки",
  viewTable: "Таблица",
  colNumber: "Номер",
  oemLabel: "OEM-код",
  oemColumn: "OEM",
  oemUnknown: "пока не указан",
  oemHelp: "Номер этой детали от завода-производителя автомобиля. По нему можно найти именно нужную деталь.",
  oemCopy: "Копировать",
  oemCopied: "Скопировано",
  oemAsk: "Знаете OEM-код? Сообщите нам",
  oemPlaceholder: "Например: 96273708",
  oemSend: "Отправить",
  oemThanks: "Спасибо! Наш специалист проверит код и добавит его на сайт.",
  oemInvalid: "Не похоже на OEM-код: нужно не меньше 5 символов и 3 цифр.",
  oemSendError: "Не удалось отправить. Попробуйте позже.",
  oemMore: (count) => `ещё ${count}`,
  faqLead: "О чём покупатели спрашивают чаще всего.",
  sellerLabel: (n) => (n > 1 ? "Продавцы" : "Продавец"),
  pickerSearch: "Поиск…",
  pickerEmpty: "Ничего не найдено",
  pickerPopular: "Популярные",
  pickerAll: "Все",
  navLabel: "На странице",
  navNumbers: "Номера",
  navCars: "Машины",
  navAlternatives: "Альтернативы",
  navTogether: "Вместе",
  seeSellers: (n) => `Смотреть продавцов (${n})`,
  colPart: "Деталь",
  colFit: "Применимость",
  colSellers: "Продавцы",
  colPrice: "Цена",
  colStock: "Наличие",
  attr_repair_size: "Ремонтный размер",
  attr_placement: "Наружный / внутренний",
  attr_transmission: "Коробка передач",
  attr_engine_type: "Двигатель",
  attr_spec_code: "Размер / код",
  val_OUTER: "Наружный",
  val_INNER: "Внутренний",
  val_AT: "Автомат (АКПП)",
  val_MT: "Механика (МКПП)",
  steps: ["Отправлено", "Подтверждено", "Готово", "Получено"],
  basketGroup: (n) => `Из корзины: ${n} ${ruPlural(n, "деталь", "детали", "деталей")}`,
  basketButton: (n) => (n ? `Корзина (${n})` : "Корзина"),
  sharedListTitle: "Список деталей, которым с вами поделились",
  sharedListAdd: "Добавить всё в мою корзину",
  tgBasket: (lines, carText, vin) => `Здравствуйте! Забронировал через MegaParts:\n${lines}\nАвтомобиль: ${carText}\nVIN: ${vin}\nНапишите, когда будет готово.`,
  promoNEW_ARRIVAL: "Новое поступление",
  promoDISCOUNT: (p) => (p ? `Скидка −${p}%` : "Акция"),
  promoPRICE_DROP: "Цена снижена",
  promoNEW_PRICE: "Новая цена",
  warrantyKm: (months, km) => `Гарантия: ${[months ? `${months} мес.` : null, km ? `${formatNumber(km)} км` : null].filter(Boolean).join(" или ")}`,
  listDate: (date) => `Прайс продавца от ${date}`,
  favSeller: "☆ В любимые продавцы",
  favSellerOn: "★ Ваш любимый продавец",
  qualityORIGINAL: "Оригинал (GM)",
  qualityKOREA: "Корея / заводское качество",
  qualityCHINA: "Китай",
  qualityBUDGET: "Эконом",
  qualityOTHER: "Другое",
  qualityTitle: "Выберите по качеству",
  qualityLead: "Один номер детали — разное качество и цена.",
  tierBest: "Самое надёжное",
  tierBetter: "Цена и качество",
  tierGood: "Экономно",
  thisPart: "Эта деталь",
  filterQuality: "Качество",
  filterBrand: "Бренд",
  sortLabel: "Сортировка",
  sortRelevance: "По соответствию",
  sortPrice: "Сначала дешёвые",
  jobsTitle: "Готовые списки для ремонта",
  jobsLead: "Выберите ремонт — покажем все нужные детали для вашей машины в одном месте.",
  jobSteps: (n) => `${n} ${ruPlural(n, "деталь", "детали", "деталей")}`,
  jobChooseCar: "Сначала выберите машину — список подстроится под неё.",
  jobAddAll: (n) => `Всё в корзину (${n})`,
  jobNone: "Пока нет в продаже",
  jobMore: (n) => `Другие варианты (${n})`,
  jobForCar: (carText) => `Для ${carText}`,
  jobAdded: "Добавлено в корзину",
  sellersTitle: "Продавцы",
  sellersLead: "Продавцы на MegaParts, их контакты и бренды, которые они продают.",
  sellerParts: (n) => `${formatNumber(n)} ${ruPlural(n, "деталь", "детали", "деталей")}`,
  sellerPriced: (n) => `из них ${formatNumber(n)} с ценой`,
  sellerOpen: "Страница продавца",
  sellerLastList: (date) => `Последний прайс: ${date}`,
  sellTitle: "Продавайте на MegaParts",
  sellLead: "У вас магазин запчастей? Оставьте заявку — примем ваш прайс (Excel) и разместим за 24 часа. Размещение бесплатное.",
  sellPoints: [
    "Покупатели находят ваши детали по своей машине",
    "Заказы приходят по телефону и в Telegram, без предоплаты",
    "Прайс в Excel может быть в любом виде — мы сами его разберём",
  ],
  sellBusiness: "Название магазина",
  sellContact: "Ваше имя",
  sellPhone: "Телефон",
  sellTelegram: "Telegram (необязательно)",
  sellCity: "Город",
  sellAddress: "Адрес (рынок, ряд)",
  sellCars: "Для каких машин продаёте детали?",
  sellNote: "Комментарий (необязательно)",
  sellSend: "Отправить заявку",
  sellSent: "Спасибо! Мы скоро свяжемся с вами.",
  sellBannerTitle: "Вы продавец?",
  sellBannerText: "Разместите свои детали на MegaParts бесплатно — покупатели найдут вас по своей машине.",
  sellBannerButton: "Подробнее",
  footerSell: "Продавать на MegaParts",
  footerSellers: "Все продавцы",
  footerJobs: "Готовые списки для ремонта",
  faqTitle: "Частые вопросы",
  faq: [
    ["Когда платить?", "Предоплаты нет. Вы бронируете деталь, продавец подтверждает, а оплачиваете вы продавцу при получении."],
    ["Как узнать, подходит ли деталь к моей машине?", "Выберите машину — на каждой детали появится отметка «Подходит» или «Проверьте». Если сомневаетесь, кнопкой «Спросить в Telegram» отправьте продавцу машину и VIN."],
    ["Можно купить у нескольких продавцов сразу?", "Да. Добавьте детали в корзину и нажмите «Забронировать всё» — каждый продавец получит свою часть."],
    ["Что значит «Оригинал», «Корея» и «Китай»?", "Оригинал — деталь автозавода (GM). Корея / заводское качество — сделано в Корее или поставщиком завода. Китай — более дешёвый аналог. Детали с одним номером сравниваются на странице детали."],
    ["А если нужной детали нет?", "Заполните запрос под результатами поиска — продавцы найдут деталь и свяжутся с вами."],
  ],
});
Object.assign(STRINGS.en, {
  basket: "Basket",
  addToBasket: "Add to basket",
  inBasket: "In basket ✓",
  basketTitle: "Your basket",
  basketLead: "Reserve parts from several sellers in one go. Each seller gets their own part of the order; you pay on collection.",
  basketEmpty: "Your basket is empty. Press “Add to basket” on a part page, or use a ready repair list.",
  basketSeller: (name) => `Seller: ${name}`,
  basketRemove: "Remove",
  basketQty: "Qty",
  basketTotal: "Total",
  basketTotalNote: "The seller will tell you the price of parts listed without one.",
  basketReserveAll: (n) => `Reserve all (${n})`,
  basketSent: "Reserved! Message each seller — the reservation numbers are already in the message.",
  basketGone: "This offer is no longer available",
  basketShare: "Share this list",
  basketShareTelegram: "Send in Telegram",
  basketCopy: "Copy link",
  basketCopied: "Link copied",
  basketShareText: (n) => `MegaParts: a list of ${n} parts`,
  basketClear: "Empty the basket",
  basketInLabel: "✓ In basket",
  basketOpen: "Open basket",
  basketRemoveFull: "Remove from basket",
  basketRemoved: (name) => `“${name}” removed from the basket.`,
  basketCleared: "The basket is empty now.",
  undo: "Undo",
  qtyLess: "Fewer",
  qtyMore: "More",
  cancelReservation: "Cancel",
  cancelConfirm: "Cancel this reservation?",
  cancelAllConfirm: "Cancel every reservation from this basket?",
  cancelYes: "Yes, cancel",
  cancelNo: "No",
  cancelAll: (n) => `Cancel all (${n})`,
  cancelled: "Cancelled. Please let the seller know too.",
  cancelError: "Could not cancel. Reload the page and try again.",
  tellSeller: "Tell the seller",
  tgCancel: (ids) => `Hello! Reservation ${ids} made through MegaParts is cancelled. Sorry.`,
  partNumber: "No.",
  refTypeOE: "OEM (carmaker number)",
  refTypeOES: "Factory supplier",
  refTypeAFTERMARKET: "Maker’s article",
  refTypeSUPPLIER_SKU: "Seller code",
  refTypeEAN: "Barcode (EAN)",
  viewCards: "Cards",
  viewTable: "Table",
  colNumber: "Number",
  oemLabel: "OEM code",
  oemColumn: "OEM",
  oemUnknown: "not known yet",
  oemHelp: "The carmaker’s own number for this part. Use it to be sure you get exactly the right part.",
  oemCopy: "Copy",
  oemCopied: "Copied",
  oemAsk: "Know the OEM code? Tell us",
  oemPlaceholder: "e.g. 96273708",
  oemSend: "Send",
  oemThanks: "Thank you! Our staff will check the code and add it to the site.",
  oemInvalid: "That doesn’t look like an OEM code: it needs at least 5 characters and 3 digits.",
  oemSendError: "Couldn’t send. Please try again later.",
  oemMore: (count) => `+${count} more`,
  faqLead: "What buyers ask us most often.",
  sellerLabel: (n) => (n > 1 ? "Sellers" : "Seller"),
  pickerSearch: "Search…",
  pickerEmpty: "Nothing found",
  pickerPopular: "Popular",
  pickerAll: "All",
  navLabel: "On this page",
  navNumbers: "Numbers",
  navCars: "Cars",
  navAlternatives: "Alternatives",
  navTogether: "Bought together",
  seeSellers: (n) => `See sellers (${n})`,
  colPart: "Part",
  colFit: "Fit",
  colSellers: "Sellers",
  colPrice: "Price",
  colStock: "Stock",
  attr_repair_size: "Repair size",
  attr_placement: "Outer / inner",
  attr_transmission: "Gearbox",
  attr_engine_type: "Engine",
  attr_spec_code: "Size / code",
  val_OUTER: "Outer",
  val_INNER: "Inner",
  val_AT: "Automatic",
  val_MT: "Manual",
  steps: ["Sent", "Confirmed", "Ready", "Collected"],
  basketGroup: (n) => `From one basket: ${n} parts`,
  basketButton: (n) => (n ? `Basket (${n})` : "Basket"),
  sharedListTitle: "A parts list shared with you",
  sharedListAdd: "Add all to my basket",
  tgBasket: (lines, carText, vin) => `Hello! I reserved these through MegaParts:\n${lines}\nCar: ${carText}\nVIN: ${vin}\nPlease let me know when they are ready.`,
  promoNEW_ARRIVAL: "New arrival",
  promoDISCOUNT: (p) => (p ? `Sale −${p}%` : "On sale"),
  promoPRICE_DROP: "Price dropped",
  promoNEW_PRICE: "New price",
  warrantyKm: (months, km) => `Warranty: ${[months ? `${months} months` : null, km ? `${formatNumber(km)} km` : null].filter(Boolean).join(" or ")}`,
  listDate: (date) => `Seller’s list of ${date}`,
  favSeller: "☆ Make favourite seller",
  favSellerOn: "★ Your favourite seller",
  qualityORIGINAL: "Original (GM)",
  qualityKOREA: "Korea / factory quality",
  qualityCHINA: "China",
  qualityBUDGET: "Budget",
  qualityOTHER: "Other",
  qualityTitle: "Choose by quality",
  qualityLead: "One part number — different quality and price.",
  tierBest: "Most reliable",
  tierBetter: "Value for money",
  tierGood: "Budget",
  thisPart: "This part",
  filterQuality: "Quality",
  filterBrand: "Brand",
  sortLabel: "Sort",
  sortRelevance: "Best match",
  sortPrice: "Cheapest first",
  jobsTitle: "Ready repair lists",
  jobsLead: "Pick a repair — we show every part it needs for your car in one place.",
  jobSteps: (n) => `${n} parts`,
  jobChooseCar: "Choose your car first — the list adapts to it.",
  jobAddAll: (n) => `Add all to basket (${n})`,
  jobNone: "Not on sale yet",
  jobMore: (n) => `Other options (${n})`,
  jobForCar: (carText) => `For ${carText}`,
  jobAdded: "Added to basket",
  sellersTitle: "Sellers",
  sellersLead: "The sellers on MegaParts, how to reach them and the brands they sell.",
  sellerParts: (n) => `${formatNumber(n)} parts`,
  sellerPriced: (n) => `${formatNumber(n)} with prices`,
  sellerOpen: "Seller page",
  sellerLastList: (date) => `Latest list: ${date}`,
  sellTitle: "Sell on MegaParts",
  sellLead: "Run a parts shop? Send an application — we take your Excel price list and put it online within 24 hours. Listing is free.",
  sellPoints: [
    "Buyers find your parts by their car",
    "Orders come by phone and Telegram, with no prepayment",
    "Your Excel list can be in any layout — we sort it out",
  ],
  sellBusiness: "Shop name",
  sellContact: "Your name",
  sellPhone: "Phone",
  sellTelegram: "Telegram (optional)",
  sellCity: "City",
  sellAddress: "Address (market, row)",
  sellCars: "Which cars do you sell parts for?",
  sellNote: "Note (optional)",
  sellSend: "Send application",
  sellSent: "Thank you! We will contact you soon.",
  sellBannerTitle: "Are you a seller?",
  sellBannerText: "List your parts on MegaParts for free — buyers find you by their car.",
  sellBannerButton: "Learn more",
  footerSell: "Sell on MegaParts",
  footerSellers: "All sellers",
  footerJobs: "Ready repair lists",
  faqTitle: "Frequently asked questions",
  faq: [
    ["When do I pay?", "There is no prepayment. You reserve the part, the seller confirms, and you pay the seller when you collect it."],
    ["How do I know a part fits my car?", "Choose your car — every part shows “Fits” or “Check”. If unsure, press “Ask in Telegram” to send the seller your car and VIN."],
    ["Can I buy from several sellers at once?", "Yes. Add the parts to the basket and press “Reserve all” — each seller gets their own part of the order."],
    ["What do “Original”, “Korea” and “China” mean?", "Original is the carmaker’s own part (GM). Korea / factory quality is made in Korea or by the factory’s supplier. China is a cheaper equivalent. Parts with the same number are compared on the part page."],
    ["What if the part I need is not listed?", "Fill in the request under the search results — sellers will find it and contact you."],
  ],
});

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
const basketView = $("#basket-view");
const jobView = $("#job-view");
const sellersView = $("#sellers-view");
const sellView = $("#sell-view");
const shopFilters = $("#shop-filters");

const PAGE_SIZE = 100;
// Reservations in 90 days before a part is marked "often reserved".
const POPULAR_AFTER = 3;
// brand, quality and sort narrow a search or a section; they reset with a new search.
const state = { query: "", category: "", all: false, spellcheck: true, brand: "", quality: "", sort: "" };
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

// replaceChildren() would print a skipped (null) child as the text "null".
const fill = (node, ...children) => node.replaceChildren(...children.filter((child) => child !== null && child !== undefined && child !== false));

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
// So'm are whole; a list priced in dollars keeps its cents ("2,47 $").
const formatPrice = (value, currency) => {
  if (!currency || currency === "UZS") return `${formatNumber(value)} ${t("som")}`;
  const amount = new Intl.NumberFormat("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Number(value));
  return currency === "USD" ? `${amount} $` : `${amount} ${currency}`;
};
const formatDate = (value) => new Date(value).toLocaleDateString(lang === "en" ? "en-GB" : "ru-RU");

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
  renderJobCards();
}

// The catalog's real size, counted from what is loaded; the numbers count up the first time.
let heroStatsKey = "";
let heroStatsCounted = false;
const countUp = (node, target) => {
  const started = performance.now();
  const step = (now) => {
    const progress = Math.min(1, (now - started) / 1100);
    node.textContent = formatNumber(Math.round(target * (1 - (1 - progress) ** 3)));
    if (progress < 1) requestAnimationFrame(step);
  };
  node.textContent = formatNumber(0);
  requestAnimationFrame(step);
};
function renderHeroStats() {
  const parts = groupsAll.reduce((sum, group) => sum + group.part_count, 0);
  const models = new Set(vehicles.map((vehicle) => `${vehicle.make}|${vehicle.model}`)).size;
  const sections = groupsAll.filter((group) => group.part_count).length;
  const stats = [[parts, "heroParts"], [models, "heroModels"], [sections, "heroSections"]].filter(([count]) => count);
  const statsKey = `${lang}|${stats.join("|")}`;
  if (statsKey === heroStatsKey) return;
  heroStatsKey = statsKey;
  const animate = stats.length && !heroStatsCounted && !reducedMotion;
  if (stats.length) heroStatsCounted = true;
  $("#hero-stats").replaceChildren(...stats.map(([count, key]) => {
    const number = el("strong", { text: formatNumber(count) });
    if (animate) countUp(number, count);
    return el("li", {}, [number, ` ${t(key, count).replace(/^\S+\s/, "")}`]);
  }));
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
  holder.replaceChildren(...top.map(([key, total]) => {
    const [make, model] = key.split("|");
    const active = car.make === make && car.model === model;
    const choose = async () => {
      await setCar({ make, model });
      $("#sections-title").scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
    };
    const tile = el("button", { type: "button", class: `car-card${active ? " is-active" : ""}`, "aria-pressed": String(active), onclick: choose });
    tile.innerHTML = '<span class="car-card-icon"></span><span class="car-card-make"></span><span class="car-card-model"></span><span class="car-card-count"></span>';
    tile.querySelector(".car-card-icon").innerHTML = CAR_ICON;
    tile.querySelector(".car-card-make").textContent = make;
    tile.querySelector(".car-card-model").textContent = vehicleLabel(model);
    tile.querySelector(".car-card-count").textContent = t("parts", total);
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

// ---------- Pickers ----------

// The site's own dropdown, drawn over a hidden native <select>. The select stays the source of
// truth: its value and "change" event drive the car and sort logic exactly as before.
let pickerSeq = 0;
let pickers = [];
function enhanceSelect(select, { search = false, includeEmpty = true, badge = null, describe = () => null, popular = () => [] } = {}) {
  const id = `picker-${++pickerSeq}`;
  const label = select.closest(".field, .sort-group")?.querySelector(".field-label, .filter-group-label");
  const valueText = el("span", { class: "picker-value", id: `${id}-value` });
  const button = el("button", { type: "button", class: "picker-button", "aria-haspopup": "listbox", "aria-expanded": "false", "aria-controls": `${id}-list` }, valueText);
  if (label) {
    label.id ||= `${id}-label`;
    button.setAttribute("aria-labelledby", `${label.id} ${id}-value`);
  } else {
    button.setAttribute("aria-label", select.getAttribute("aria-label") || "");
  }
  const input = search ? el("input", { class: "picker-search", type: "search", autocomplete: "off", spellcheck: "false", role: "combobox", "aria-expanded": "true", "aria-controls": `${id}-list`, "aria-autocomplete": "list" }) : null;
  const searchRow = input ? el("div", { class: "picker-search-row" }, input) : null;
  const list = el("div", { class: "picker-list", role: "listbox", id: `${id}-list`, tabindex: "-1" });
  const panel = el("div", { class: "picker-panel", hidden: true }, [searchRow, list]);
  const wrapper = el("div", { class: "picker" }, [button, panel]);
  select.after(wrapper);
  select.classList.add("picker-native");
  select.tabIndex = -1;
  select.setAttribute("aria-hidden", "true");

  let items = [];
  let active = -1;
  const isOpen = () => !panel.hidden;
  const keyTarget = () => input || list;
  const options = () => [...select.options]
    .map((option) => ({ value: option.value, text: option.textContent }))
    .filter((option) => option.value || includeEmpty);

  function showActive() {
    list.querySelectorAll(".picker-option").forEach((node, index) => node.classList.toggle("is-active", index === active));
    const node = list.querySelectorAll(".picker-option")[active];
    if (node) {
      keyTarget().setAttribute("aria-activedescendant", node.id);
      node.scrollIntoView({ block: "nearest" });
    } else {
      keyTarget().removeAttribute("aria-activedescendant");
    }
  }

  function render() {
    const all = options();
    if (searchRow) searchRow.hidden = all.length <= 7;
    const words = (input?.value || "").trim().toLowerCase();
    const matches = all.filter((option) => !words || option.text.toLowerCase().includes(words));
    const favourites = words ? [] : popular().map((value) => all.find((option) => option.value === value)).filter(Boolean);
    items = [...favourites, ...matches];
    const row = (option, index) => el("div", {
      role: "option",
      id: `${id}-option-${index}`,
      class: `picker-option${option.value === select.value ? " is-selected" : ""}${option.value ? "" : " is-empty"}`,
      "aria-selected": String(option.value === select.value),
      onclick: () => choose(option.value),
    }, [
      badge && option.value ? el("span", { class: "picker-badge", "aria-hidden": "true", text: badge(option) }) : null,
      el("span", { class: "picker-text", text: option.text }),
      describe(option.value) ? el("span", { class: "picker-meta", text: describe(option.value) }) : null,
      el("span", { class: "picker-check", "aria-hidden": "true", text: "✓" }),
    ]);
    const nodes = items.map(row);
    nodes.forEach((node, index) => node.addEventListener("mousemove", () => { if (active !== index) { active = index; showActive(); } }));
    const heading = (text) => el("div", { class: "picker-group", role: "presentation", text });
    list.replaceChildren(...(favourites.length
      ? [heading(t("pickerPopular")), ...nodes.slice(0, favourites.length), heading(t("pickerAll")), ...nodes.slice(favourites.length)]
      : nodes));
    if (!items.length) list.append(el("div", { class: "picker-empty", text: t("pickerEmpty") }));
    active = Math.min(Math.max(active, 0), items.length - 1);
    showActive();
  }

  function close(focusButton = false) {
    if (!isOpen()) return;
    panel.hidden = true;
    wrapper.classList.remove("is-open");
    button.setAttribute("aria-expanded", "false");
    if (focusButton) button.focus();
  }

  function open(typed = "") {
    if (button.disabled || isOpen()) return;
    pickers.forEach((picker) => picker.close());
    panel.hidden = false;
    wrapper.classList.add("is-open");
    button.setAttribute("aria-expanded", "true");
    if (input) {
      input.placeholder = t("pickerSearch");
      input.value = typed;
    }
    active = -1;
    render();
    active = typed ? 0 : Math.max(0, items.findIndex((option) => option.value === select.value));
    showActive();
    keyTarget().focus({ preventScroll: true });
  }

  function choose(value) {
    close(true);
    if (select.value === value) return;
    select.value = value;
    select.dispatchEvent(new Event("change", { bubbles: true }));
  }

  button.addEventListener("click", () => (isOpen() ? close() : open()));
  button.addEventListener("keydown", (event) => {
    if (["ArrowDown", "ArrowUp", "Enter", " "].includes(event.key)) {
      event.preventDefault();
      open();
    } else if (input && event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      open(event.key);
    }
  });
  input?.addEventListener("input", () => { active = 0; render(); });
  keyTarget().addEventListener("keydown", (event) => {
    const last = items.length - 1;
    if (event.key === "ArrowDown") active = Math.min(last, active + 1);
    else if (event.key === "ArrowUp") active = Math.max(0, active - 1);
    else if (event.key === "Home" && !input) active = 0;
    else if (event.key === "End" && !input) active = last;
    else if (event.key === "Enter") {
      event.preventDefault();
      if (items[active]) choose(items[active].value);
      return;
    } else if (event.key === "Escape") {
      event.preventDefault();
      event.stopPropagation();
      close(true);
      return;
    } else if (event.key === "Tab") {
      close();
      return;
    } else {
      return;
    }
    event.preventDefault();
    showActive();
  });

  function refresh() {
    const current = select.options[select.selectedIndex];
    valueText.textContent = current?.textContent || "";
    button.classList.toggle("is-placeholder", !select.value);
    button.disabled = select.disabled;
    if (button.disabled) close();
    else if (isOpen()) render();
  }

  const picker = { select, button, wrapper, refresh, close };
  pickers = [...pickers.filter((known) => known.wrapper.isConnected), picker];
  refresh();
  return picker;
}
const refreshPickers = () => pickers.forEach((picker) => picker.refresh());
document.addEventListener("click", (event) => {
  pickers.forEach((picker) => { if (!event.composedPath().includes(picker.wrapper)) picker.close(); });
});

// ---------- Car ----------

const option = (value, label) => el("option", { value, text: label });

function fillSelect(select, placeholder, entries, selected) {
  select.replaceChildren(option("", placeholder), ...entries.map(([value, label]) => option(value, label)));
  select.value = entries.some(([value]) => value === selected) ? selected : "";
}

// How many parts each make, model and generation has, for the pickers.
const carPickerCounts = { makes: new Map(), models: new Map(), generations: new Map() };
const countLabel = (count) => (count ? t("parts", count) : null);
const topValues = (counts, limit) => [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit).map(([value]) => value);
const initials = (option) => option.text.split(/\s+/).slice(0, 2).map((word) => word[0]).join("").toUpperCase();
const makePicker = enhanceSelect(carMake, {
  search: true,
  includeEmpty: false,
  badge: initials,
  describe: (make) => countLabel(carPickerCounts.makes.get(make)),
  popular: () => (carPickerCounts.makes.size > 6 ? topValues(carPickerCounts.makes, 4) : []),
});
const modelCounts = () => new Map([...carPickerCounts.models.entries()]
  .filter(([key]) => key.startsWith(`${carMake.value}|`))
  .map(([key, count]) => [key.slice(carMake.value.length + 1), count]));
enhanceSelect(carModel, {
  search: true,
  describe: (model) => countLabel(modelCounts().get(model)),
  popular: () => (modelCounts().size > 7 ? topValues(modelCounts(), 3) : []),
});
enhanceSelect(carGeneration, { describe: (id) => countLabel(carPickerCounts.generations.get(id)) });

function renderGarage() {
  carPickerCounts.makes.clear();
  carPickerCounts.models.clear();
  carPickerCounts.generations.clear();
  vehicles.forEach((vehicle) => {
    carPickerCounts.makes.set(vehicle.make, (carPickerCounts.makes.get(vehicle.make) || 0) + vehicle.part_count);
    const model = `${vehicle.make}|${vehicle.model}`;
    carPickerCounts.models.set(model, (carPickerCounts.models.get(model) || 0) + vehicle.part_count);
    carPickerCounts.generations.set(vehicle.id, vehicle.part_count);
  });
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
  refreshPickers();
  $("#car-toggle-label").textContent = hasCar() ? carLabel() : t("footerChooseCar");
  $("#car-toggle").classList.toggle("has-car", hasCar());
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
  else if (!jobView.hidden && currentJobId) showJob(currentJobId, false);
  else if (!resultsView.hidden || !loading.hidden) navigate({ ...state, push: false });
}

carMake.addEventListener("change", () => setCar(carMake.value ? { make: carMake.value } : {}, { refining: true }));
carModel.addEventListener("change", () => setCar(carModel.value ? { make: car.make, model: carModel.value } : { make: car.make }, { refining: true }));
carGeneration.addEventListener("change", () => setCar(
  carGeneration.value ? { make: car.make, model: car.model, vehicle_id: carGeneration.value, vin: car.vin } : { make: car.make, model: car.model, vin: car.vin },
  { refining: true },
));
carClear.addEventListener("click", () => setCar({}));

// Off the home page the car picker folds into a button above the results.
function setCarPanel(open) {
  $("#finder").classList.toggle("is-car-open", open);
  $("#car-toggle").setAttribute("aria-expanded", String(open));
}
$("#car-toggle").addEventListener("click", () => setCarPanel(!$("#finder").classList.contains("is-car-open")));
document.addEventListener("click", (event) => {
  if (!event.composedPath().includes($(".finder-car"))) setCarPanel(false);
});
document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape" || !$("#finder").classList.contains("is-car-open")) return;
  setCarPanel(false);
  $("#car-toggle").focus();
});
// "Choose your car" links open the picker wherever it is. The click stops here, or the
// "click outside closes it" rule above would shut the panel straight away.
function openCarPicker(event) {
  event?.stopPropagation();
  if (document.body.classList.contains("view-home")) {
    $("#step-car-title").scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "center" });
  } else {
    window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" });
    setCarPanel(true);
  }
  makePicker.button.focus({ preventScroll: true });
}
document.querySelectorAll('a[href="#step-car-title"]').forEach((link) => link.addEventListener("click", (event) => {
  event.preventDefault();
  openCarPicker(event);
}));

// ---------- Views ----------

const showOnly = (element) => {
  if (element !== detailView) document.title = t("pageTitle");
  // The full welcome area is for the home page; other views get a compact top.
  document.body.classList.toggle("view-home", element === browseView);
  [browseView, loading, errorBox, resultsView, detailView, reservationsView, basketView, jobView, sellersView, sellView]
    .forEach((node) => { node.hidden = node !== element; });
};

// A part lives at /part/{id}, the address search engines index; the search stays in ?q=.
const urlFor = (product) => {
  const params = new URLSearchParams();
  if (state.query) params.set("q", state.query);
  if (state.category) params.set("cat", state.category);
  if (state.all && !state.query && !state.category) params.set("all", "1");
  if (state.brand) params.set("brand", state.brand);
  if (state.quality) params.set("quality", state.quality);
  if (state.sort) params.set("sort", state.sort);
  const search = params.toString();
  const path = product ? `/part/${encodeURIComponent(product)}` : "/";
  return search ? `${path}?${search}` : path;
};

function showHome(push = true) {
  Object.assign(state, { query: "", category: "", all: false, spellcheck: true, brand: "", quality: "", sort: "" });
  input.value = "";
  if (push) history.pushState(null, "", "/");
  renderGroups();
  renderJobCards();
  showOnly(browseView);
}

function navigate({ query = state.query, category = state.category, all = false, spellcheck = true, push = true, brand = "", quality = "", sort = state.sort } = {}) {
  Object.assign(state, { query: query.trim(), category, all, spellcheck, brand: String(brand || ""), quality, sort });
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
  if (state.brand) params.set("brand", state.brand);
  if (state.quality) params.set("quality", state.quality);
  if (state.sort) params.set("sort", state.sort);
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
  renderShopFilters();
  $("#results-layout").classList.toggle("no-side", !typeFilter.childElementCount && shopFilters.hidden);
  renderSpelling();

  results.replaceChildren();
  renderLayoutToggle();
  $("#layout-toggle").hidden = !data.total;
  const table = resultsLayout === "table" && data.items.length;
  results.classList.toggle("is-table", Boolean(table));
  if (table) {
    // Similar (RELATED) parts stay below the matches, under their own heading.
    const main = data.items.filter((item) => item.result_group !== "RELATED" || !data.query);
    const related = data.items.filter((item) => item.result_group === "RELATED" && data.query);
    if (main.length) results.append(resultsTable(main));
    if (related.length) results.append(el("h3", { class: "related-heading", text: t("related") }), resultsTable(related));
  }
  let relatedShown = false;
  (table ? [] : data.items).forEach((item) => {
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

// The number professionals search by: the carmaker's (OEM) first, then the part maker's;
// a seller's own code only when there is nothing else.
const NUMBER_ORDER = ["OE", "OES", "AFTERMARKET", "EAN", "SUPPLIER_SKU"];
const sortedNumbers = (item) => [...(item.reference_numbers || [])]
  .sort((a, b) => NUMBER_ORDER.indexOf(a.type) - NUMBER_ORDER.indexOf(b.type));
// A part is described by the company that sells it first, then the brand that made it.
const sellerNames = (offers) => [...new Set((offers || []).map((offer) => supplierLabel(offer.supplier)))];
const sellerText = (offers, max = 2) => {
  const names = sellerNames(offers);
  return names.length > max ? `${names.slice(0, max).join(", ")} +${names.length - max}` : names.join(", ");
};

// Every part shows its OEM (carmaker's) code, or says it is not known yet.
const isOem = (ref) => ref.type === "OE" || ref.type === "OES";
const oemNumbers = (item) => sortedNumbers(item).filter(isOem).map((ref) => ref.number);
const otherNumber = (item) => sortedNumbers(item).find((ref) => !isOem(ref));

function oemCell(item) {
  const oem = oemNumbers(item);
  if (oem.length) return el("span", { class: "mono", text: oem.slice(0, 2).join(", ") });
  const other = otherNumber(item);
  return el("span", { class: "muted" }, ["—", other ? el("small", { class: "table-sub", text: `${t(`refType${other.type}`)}: ${other.number}` }) : null]);
}

// Part page: the OEM code up top with a copy button; without one, buyers and mechanics who
// know it can send it in (staff check it before it is shown).
function oemBlock(item) {
  const oem = oemNumbers(item);
  const head = [el("span", { class: "oem-label", text: t("oemLabel") })];
  const help = el("p", { class: "oem-help", text: t("oemHelp") });
  if (oem.length) {
    const status = el("span", { class: "oem-status", role: "status" });
    const copy = el("button", {
      type: "button",
      class: "link-button oem-copy",
      text: t("oemCopy"),
      onclick: async () => {
        try { await navigator.clipboard.writeText(oem.join(", ")); status.textContent = t("oemCopied"); } catch { status.textContent = oem.join(", "); }
      },
    });
    return el("div", { class: "oem-block" }, [
      el("div", { class: "oem-row" }, [...head, ...oem.map((number) => el("strong", { class: "mono oem-number", text: number })), copy, status]),
      help,
    ]);
  }
  const slot = el("div", { class: "oem-ask" });
  const openForm = () => {
    const input = el("input", { class: "oem-input", inputmode: "text", autocomplete: "off", maxlength: "60", placeholder: t("oemPlaceholder"), "aria-label": t("oemLabel") });
    const message = el("p", { class: "oem-message", role: "status" });
    const form = el("form", { class: "oem-form" }, [input, el("button", { class: "secondary-button", text: t("oemSend") }), message]);
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const code = input.value.replace(/[^0-9a-z]/gi, "");
      if (code.length < 5 || (code.match(/\d/g) || []).length < 3) {
        message.textContent = t("oemInvalid");
        return;
      }
      try {
        const response = await postJson(`/api/v1/products/${encodeURIComponent(item.id)}/oem-suggestions`, { number: input.value.trim(), session_id: pilotSessionId });
        if (response.ok) slot.replaceChildren(el("p", { class: "oem-thanks", text: t("oemThanks") }));
        else message.textContent = t(response.status === 422 ? "oemInvalid" : "oemSendError");
      } catch {
        message.textContent = t("oemSendError");
      }
    });
    slot.replaceChildren(form);
    input.focus();
  };
  slot.append(el("button", { type: "button", class: "link-button", text: t("oemAsk"), onclick: openForm }));
  return el("div", { class: "oem-block is-unknown" }, [
    el("div", { class: "oem-row" }, [...head, el("span", { class: "oem-unknown", text: t("oemUnknown") })]),
    help,
    slot,
  ]);
}

async function openFromResults(item) {
  currentProductId = item.id;
  if (currentEventId) {
    try { await postJson(`/api/search-events/${currentEventId}/click`, { product_id: item.id }); } catch { /* analytics only */ }
  }
  openProduct(item.id);
}

// Shops and mechanics compare many parts at once: number, part, brand, fit, sellers, stock, price.
let resultsLayout = storage.get("megaparts_results_layout") === "table" ? "table" : "cards";
function renderLayoutToggle() {
  $("#layout-toggle").replaceChildren(...["cards", "table"].map((mode) => el("button", {
    type: "button",
    class: `layout-button${resultsLayout === mode ? " is-active" : ""}`,
    "aria-pressed": String(resultsLayout === mode),
    text: t(mode === "cards" ? "viewCards" : "viewTable"),
    onclick: () => {
      resultsLayout = mode;
      storage.set("megaparts_results_layout", mode);
      renderResults();
    },
  })));
}

function resultsTable(items) {
  const headings = [t("oemColumn"), t("colPart"), t("colSellers"), t("brand"), t("colFit"), t("colStock"), t("colPrice")];
  const rows = items.map((item) => {
    const offers = item.offers || item.supplier_offers || [];
    const price = priceSummary(offers);
    const stock = stockSummary(offers);
    const verdict = fitVerdict(item);
    const row = el("tr", { class: `result-row${item.result_group === "RELATED" ? " is-related" : ""}`, tabindex: "0", onclick: () => openFromResults(item) }, [
      el("td", {}, oemCell(item)),
      el("td", {}, [
        el("strong", { class: "table-name", text: productName(item) }),
        el("span", { class: "table-sub", text: localName(item.category) }),
      ]),
      el("td", { class: "table-sellers", text: sellerText(offers, 3) || "—" }),
      el("td", {}, [el("span", { text: brandLabel(item.brand) }), " ", qualityBadge(item.quality)]),
      el("td", {}, el("span", { class: `table-fit is-${verdict.tone}`, text: `${VERDICT_ICON[verdict.tone]} ${verdict.title}` })),
      el("td", {}, el("span", { class: `stock stock-${stock.tone}`, text: stock.text })),
      el("td", { class: `num${price.known ? "" : " muted"}`, text: price.text }),
    ]);
    row.addEventListener("keydown", (event) => { if (event.key === "Enter") openFromResults(item); });
    return row;
  });
  return el("div", { class: "table-scroll" }, el("table", { class: "results-table" }, [
    el("thead", {}, el("tr", {}, headings.map((label) => el("th", { scope: "col", text: label })))),
    el("tbody", {}, rows),
  ]));
}

function resultCard(item) {
  const offers = item.offers || item.supplier_offers || [];
  const price = priceSummary(offers);
  const stock = stockSummary(offers);
  const place = placeLabel(item);
  const oem = oemNumbers(item);
  const other = oem.length ? null : otherNumber(item);
  const chip = (label, value, extra = "") => el("span", { class: `meta-chip${extra}` }, [el("span", { class: "meta-label", text: label }), value]);
  return el("article", { class: "result-card", onclick: () => openFromResults(item) }, [
    el("div", { class: "result-head" }, [
      partThumb(item.category),
      el("div", { class: "result-head-text" }, [
        el("div", { class: "result-topline" }, [
          el("p", { class: "result-type", text: localName(item.category) }),
          item.reservation_count >= POPULAR_AFTER ? el("span", { class: "popular-badge", text: t("oftenReserved") }) : null,
        ]),
        el("h3", { class: "result-name", text: productName(item) }),
      ]),
    ]),
    el("div", { class: "result-meta" }, [
      offers.length ? chip(t("sellerLabel", sellerNames(offers).length), el("strong", { text: sellerText(offers) }), " is-seller") : null,
      chip(t("brand"), el("strong", {}, [brandLabel(item.brand), " ", qualityBadge(item.quality)])),
      oem.length
        ? chip("OEM", el("strong", { class: "mono", text: oem.length > 1 ? `${oem[0]} +${oem.length - 1}` : oem[0] }), " is-oem")
        : chip("OEM", el("span", { text: t("oemUnknown") }), " is-oem is-unknown"),
      other ? chip(t(`refType${other.type}`), el("strong", { class: "mono", text: other.number })) : null,
      place ? el("span", { class: "meta-chip is-place", text: place }) : null,
    ]),
    verdictNode(fitVerdict(item), true),
    el("div", { class: "result-bottom" }, [
      el("div", { class: "result-price-block" }, [
        el("div", { class: `result-price${price.known ? "" : " is-unknown"}`, text: price.text }),
        el("div", { class: `stock stock-${stock.tone}`, text: stock.text }),
      ]),
      offers.length ? el("span", { class: "result-offers", text: t("offerCount", offers.length) }) : null,
      el("button", { type: "button", class: "details-button", text: `${t("details")} →` }),
    ]),
  ]);
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
    if (related.relation === "SAME_NUMBER") {
      return t(related.same_variant === false ? "sameNumberVariant" : "sameNumber", related.shared_number);
    }
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
  offer.warranty_km ? t("warrantyKm", offer.warranty_months, offer.warranty_km) : offer.warranty_months ? t("warranty", offer.warranty_months) : null,
  offer.return_days ? t("returns", offer.return_days) : null,
].filter(Boolean);
// The seller's own label from their list: "Yangi keldi", "Aksiya −20%".
const promoLabel = (offer) => (offer.promo ? t(`promo${offer.promo}`, offer.discount_percent) : null);

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
    fill(
      followUp,
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
  const promo = promoLabel(offer);
  // A list naming parts without price or stock only says the seller carries the part.
  const listedOnly = offer.price == null && offer.stock_qty == null;
  const outdated = !listedOnly && offer.freshness_status === "OUTDATED";
  const ageDays = offer.updated_at ? Math.round((Date.now() - new Date(offer.updated_at).getTime()) / 86400000) : 0;
  const reserveButton = el("button", { type: "button", class: "secondary-button", text: t("reserve") });
  const formNode = reserveForm(offer, reserveButton, item);
  reserveButton.addEventListener("click", () => { reserveButton.hidden = true; formNode.hidden = false; formNode.querySelector("input").focus(); });
  const basketSlot = el("div", { class: "basket-slot" });
  const showBasketState = () => basketSlot.replaceChildren(basketControl(offer.id, item.id, showBasketState, () => recordAction("basket_add", offer)));
  showBasketState();
  const favourite = el("button", { type: "button", class: "fav-seller" });
  const showFavourite = () => {
    const on = favSellers.has(offer.supplier.id);
    favourite.textContent = on ? t("favSellerOn") : t("favSeller");
    favourite.setAttribute("aria-pressed", String(on));
  };
  favourite.addEventListener("click", () => { toggleFavSeller(offer.supplier.id); showFavourite(); });
  showFavourite();
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
  const freshness = listedOnly && offer.updated_at ? t("listDate", formatDate(offer.updated_at)) : outdated ? t("outdated", ageDays) : freshnessLabel(offer);
  return el("div", { class: `offer${outdated ? " is-outdated" : ""}${favSellers.has(offer.supplier.id) ? " is-favourite" : ""}` }, [
    el("div", { class: "offer-supplier", text: supplierLabel(offer.supplier) }),
    favourite,
    sellerTrust(offer.supplier),
    offer.supplier_sku ? el("div", { class: "offer-code", text: offer.supplier_sku }) : null,
    promo ? el("span", { class: `offer-promo is-${offer.promo.toLowerCase()}`, text: promo }) : null,
    labels.length ? el("div", { class: "offer-labels" }, labels.map((label) => el("span", { class: "offer-label", text: label }))) : null,
    el("div", { class: "offer-row" }, [
      el("span", { class: "price", text: price }),
      el("span", { class: `stock stock-${stock.tone}`, text: leadTime && stock.tone !== "in" ? leadTime : stock.text }),
    ]),
    el("div", { class: "offer-freshness", text: freshness }),
    pilotMode && offer.data_status === "DEMO" ? el("div", { class: "offer-demo", text: t("testData") }) : null,
    basketSlot,
    el("div", { class: "offer-actions" }, actions),
    formNode,
  ]);
}

let offersObserver = null;
function renderDetail() {
  const item = lastDetail;
  currentProductId = item.id;
  const back = el("button", {
    type: "button",
    class: "back secondary-button",
    text: t("back"),
    onclick: () => (lastResponse ? history.back() : showHome()),
  });

  const facts = [[t("partType"), localName(item.category)], [t("position"), item.position && (t(item.position) || item.position)], [t("side"), item.side && (t(item.side) || item.side)], [t("origin"), CatalogText.originLabel(item.origin, lang)], [t("filterQuality"), item.quality && item.quality !== "OTHER" ? t(`quality${item.quality}`) : null],
    // The part's attributes read from sellers' names (repair size, outer/inner, gearbox…).
    ...(item.attributes || [])
      .filter((attribute) => ["repair_size", "placement", "transmission", "engine_type", "spec_code"].includes(attribute.attribute_code))
      .map((attribute) => [t(`attr_${attribute.attribute_code}`), t(`val_${attribute.value}`) || attribute.value])]
    .filter(([, value]) => value)
    .map(([label, value]) => el("div", { class: "fact" }, [el("span", { text: label }), el("strong", { text: value })]));

  // Each number says what it is: the carmaker's, the part maker's, or a seller's own code.
  const references = item.reference_numbers.length
    ? sortedNumbers(item).map((ref) => el("span", { class: `reference is-${ref.type.toLowerCase()}` }, [
      ref.number,
      el("small", { class: "reference-type", text: t(`refType${ref.type}`) || ref.type }),
    ]))
    : [el("p", { class: "muted", text: t("noReferences") })];

  const fitmentLine = (fitment) => {
    const place = [fitment.position, fitment.side].filter(meaningful).map((value) => t(value) || value).join(" · ");
    return el("div", { class: "fitment" }, [
      el("span", { text: vehicleLabel([fitment.vehicle.make, fitment.vehicle.model, fitment.vehicle.generation].filter(Boolean).join(" · ")) }),
      place ? el("span", { class: "fitment-note", text: place }) : null,
      fitment.condition_note ? el("span", { class: "fitment-note", text: `${t("fitCondition")}: ${noteLabel(fitment.condition_note)}` }) : null,
    ]);
  };
  // Several sellers can list the same car; it is shown once.
  const fitments = [...new Map(item.vehicle_fitments.map((fitment) => [fitment.vehicle.id, fitment])).values()];
  const cars = item.universal
    ? [el("div", { class: "fitment is-match", text: t("fitsAll") })]
    : fitments.length
      ? fitments.map(fitmentLine)
      : [el("p", { class: "muted", text: t("fitsUnknown") })];

  // The buyer's favourite sellers first; otherwise the server's order (in stock, reliable).
  const offerItems = [...(item.offers || item.supplier_offers)]
    .sort((a, b) => Number(favSellers.has(b.supplier.id)) - Number(favSellers.has(a.supplier.id)));
  const alternatives = relatedSection(t("alternativesTitle"), item.alternatives);
  const together = relatedSection(t("completeJobTitle"), item.complete_the_job);
  if (alternatives) alternatives.id = "detail-alternatives";
  if (together) together.id = "detail-together";
  const goTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
  const sectionLinks = [
    ["detail-numbers", t("navNumbers")],
    ["detail-cars", t("navCars")],
    alternatives ? ["detail-alternatives", t("navAlternatives")] : null,
    together ? ["detail-together", t("navTogether")] : null,
    ["detail-offers", t("sellers", offerItems.length)],
  ].filter(Boolean);

  const top = el("header", { class: "detail-top" }, [
    el("div", { class: "detail-head" }, [
      partThumb(item.category, true),
      el("div", { class: "detail-head-text" }, [
        el("div", { class: "detail-topline" }, [
          el("p", { class: "detail-type", text: localName(item.category) }),
          item.reservation_count >= POPULAR_AFTER ? el("span", { class: "popular-badge", text: t("oftenReserved") }) : null,
        ]),
        el("h2", { text: productName(item) }),
        el("dl", { class: "detail-origin" }, [
          offerItems.length ? el("div", {}, [
            el("dt", { text: t("sellerLabel", sellerNames(offerItems).length) }),
            el("dd", { text: sellerNames(offerItems).join(", ") }),
          ]) : null,
          el("div", {}, [el("dt", { text: t("brand") }), el("dd", { text: brandLabel(item.brand) })]),
        ]),
      ]),
    ]),
    el("div", { class: "detail-top-facts" }, [oemBlock(item), verdictNode(fitVerdict(item))]),
    el("nav", { class: "detail-nav", "aria-label": t("navLabel") }, sectionLinks.map(([id, label]) => el("a", {
      href: `#${id}`,
      class: "detail-nav-link",
      text: label,
      onclick: (event) => { event.preventDefault(); goTo(id); },
    }))),
  ]);

  const main = el("article", { class: "detail-main" }, [
    qualityChoices(item),
    askSellerBox(item, offerItems),
    facts.length ? el("div", { class: "facts" }, facts) : null,
    el("section", { class: "detail-section", id: "detail-numbers" }, [el("h3", { text: t("referenceNumbers") }), el("div", { class: "reference-list" }, references)]),
    el("section", { class: "detail-section", id: "detail-cars" }, [el("h3", { text: t("fitments") }), el("div", { class: "fitment-list" }, cars)]),
    fitFeedback(item),
    alternatives,
    together,
    currentEventId && pilotMode ? feedbackPanel() : null,
  ]);

  const offers = el("aside", { class: "offers-panel", id: "detail-offers" }, [
    el("h3", { text: t("sellers", offerItems.length) }),
    ...offerItems.map((offer) => offerNode(offer, item)),
    offerItems.length ? null : el("p", { class: "muted", text: t("noOffers") }),
  ]);

  // On phones the sellers come after the whole description: a button jumps there until they show.
  const jump = offerItems.length ? el("button", { type: "button", class: "offers-jump", onclick: () => goTo("detail-offers") }, [t("seeSellers", offerItems.length), el("span", { "aria-hidden": "true", text: " ↓" })]) : null;
  offersObserver?.disconnect();
  if (jump && "IntersectionObserver" in window) {
    offersObserver = new IntersectionObserver(([entry]) => jump.classList.toggle("is-hidden", entry.isIntersecting), { threshold: 0.02 });
    offersObserver.observe(offers);
  }

  fill(detailView, back, top, el("div", { class: "detail-shell" }, [main, offers]), jump);
  document.title = `${productName(item)} — MegaParts`;
  showOnly(detailView);
}

// An empty page says what is missing and offers the next step.
const EMPTY_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="m3 7.5 9 4.5 9-4.5M12 12v9"/></svg>';
function emptyState(text) {
  const icon = el("span", { class: "empty-icon" });
  icon.innerHTML = EMPTY_ICON;
  return el("div", { class: "empty-state" }, [
    icon,
    el("p", { text }),
    el("button", { type: "button", class: "primary-button", text: t("browseSections"), onclick: () => showHome() }),
  ]);
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
  const open = OPEN_STATUSES.includes(reservation.status);
  return el("article", { class: "reservation-card" }, [
    el("span", { class: `reservation-status is-${reservation.status.toLowerCase()}`, text: t(`status${reservation.status}`) || reservation.status }),
    statusSteps(reservation.status),
    el("h3", {}, [el("button", { type: "button", class: "link-button", text: productName(reservedProduct), onclick: () => openProduct(reservation.product_id) })]),
    el("p", { class: "muted", text: [`№${reservation.id}`, created, t("quantityShort", reservation.quantity), reservation.vehicle_label, reservation.vin].filter(Boolean).join(" · ") }),
    el("p", {}, [el("strong", { text: supplierLabel(supplier) }), reservation.price != null ? ` · ${formatPrice(reservation.price, reservation.currency)}` : ""]),
    justCancelled.has(reservation.id) ? cancelledNotice([reservation]) : null,
    el("div", { class: "reserve-actions" }, [
      open && supplier.telegram ? el("a", { class: "primary-button", href: telegramLink(supplier.telegram, message), target: "_blank", rel: "noopener", text: t("messageSeller") }) : null,
      open && supplier.phone ? el("a", { class: "secondary-button", href: `tel:${supplier.phone}`, text: t("call") }) : null,
      open ? cancelControl(t("cancelReservation"), t("cancelConfirm"), () => cancelReservations(`/api/v1/reservations/${reservation.id}/cancel`)) : null,
    ]),
  ]);
}

// ---------- Cancelling a reservation ----------

// A buyer can cancel until the part is collected; the seller is not marked unreliable for it.
const OPEN_STATUSES = ["REQUESTED", "CONFIRMED", "READY"];
const justCancelled = new Set();

// A cancel button that asks once more before it acts.
function cancelControl(label, question, run) {
  const slot = el("div", { class: "cancel-control" });
  const ask = () => slot.replaceChildren(
    el("span", { class: "cancel-question", text: question }),
    el("button", {
      type: "button",
      class: "danger-button",
      text: t("cancelYes"),
      onclick: async (event) => {
        event.currentTarget.disabled = true;
        if (!(await run())) slot.replaceChildren(el("span", { class: "reserve-status is-error", text: t("cancelError") }));
      },
    }),
    el("button", { type: "button", class: "secondary-button", text: t("cancelNo"), onclick: idle }),
  );
  const idle = () => slot.replaceChildren(el("button", { type: "button", class: "link-button cancel-link", text: label, onclick: ask }));
  idle();
  return slot;
}

async function cancelReservations(url) {
  let updated = null;
  try {
    const response = await postJson(url, { session_id: pilotSessionId });
    if (response.ok) updated = await response.json();
  } catch { /* reported by the caller */ }
  if (!updated) return false;
  [].concat(updated).forEach((reservation) => {
    justCancelled.add(reservation.id);
    const index = myReservations.findIndex((entry) => entry.id === reservation.id);
    if (index >= 0) myReservations[index] = reservation;
  });
  renderReservations();
  return true;
}

// After cancelling: a ready Telegram message so the seller stops keeping the part.
function cancelledNotice(reservations) {
  const { supplier } = reservations[0];
  const ids = reservations.map((reservation) => `№${reservation.id}`).join(", ");
  return el("div", { class: "cancelled-notice", role: "status" }, [
    el("span", { text: t("cancelled") }),
    supplier.telegram ? el("a", { class: "secondary-button", href: telegramLink(supplier.telegram, t("tgCancel", ids)), target: "_blank", rel: "noopener", text: t("tellSeller") }) : null,
    supplier.phone ? el("a", { class: "secondary-button", href: `tel:${supplier.phone}`, text: t("call") }) : null,
  ]);
}

const STATUS_ORDER = ["REQUESTED", "CONFIRMED", "READY", "COMPLETED"];
// Where the reservation is: sent, confirmed by the seller, ready, collected.
function statusSteps(status) {
  const reached = STATUS_ORDER.indexOf(status);
  if (reached < 0) return null;
  return el("ol", { class: "status-steps", "aria-label": t(`status${status}`) }, t("steps").map((label, index) => el("li", {
    class: index < reached ? "is-done" : index === reached ? "is-current" : "",
    "aria-current": index === reached ? "step" : null,
    text: label,
  })));
}

function renderReservations() {
  // Reservations sent together from the basket stay together.
  const groups = [];
  const byBasket = new Map();
  myReservations.forEach((reservation) => {
    if (!reservation.basket_id) {
      groups.push([reservation]);
      return;
    }
    if (!byBasket.has(reservation.basket_id)) {
      byBasket.set(reservation.basket_id, []);
      groups.push(byBasket.get(reservation.basket_id));
    }
    byBasket.get(reservation.basket_id).push(reservation);
  });
  reservationsView.replaceChildren(
    el("button", { type: "button", class: "back secondary-button", text: t("back"), onclick: () => showHome() }),
    el("h2", { class: "page-title", text: t("myReservations") }),
    myReservations.length
      ? el("div", { class: "reservation-list" }, groups.map((group) => {
        if (group.length === 1) return reservationCard(group[0]);
        const stillOpen = group.filter((reservation) => OPEN_STATUSES.includes(reservation.status));
        return el("section", { class: "reservation-basket" }, [
          el("div", { class: "reservation-basket-head" }, [
            el("h3", { class: "reservation-basket-title", text: t("basketGroup", group.length) }),
            stillOpen.length > 1 ? cancelControl(t("cancelAll", stillOpen.length), t("cancelAllConfirm"), () => cancelReservations(`/api/v1/reservations/basket/${encodeURIComponent(group[0].basket_id)}/cancel`)) : null,
          ]),
          ...group.map(reservationCard),
        ]);
      }))
      : emptyState(t("noReservations")),
  );
  showOnly(reservationsView);
}

$("#my-reservations").addEventListener("click", () => showReservations());
$("#footer-year").textContent = `© ${new Date().getFullYear()}`;

// ---------- Quality grades ----------

const QUALITY_ORDER = ["ORIGINAL", "KOREA", "CHINA", "BUDGET", "OTHER"];
const qualityBadge = (quality) => (quality && quality !== "OTHER"
  ? el("span", { class: `quality-badge is-${quality.toLowerCase()}`, text: t(`quality${quality}`) })
  : null);
const lowestOffer = (offers) => {
  const priced = (offers || []).filter((offer) => offer.price != null);
  return priced.length ? priced.reduce((best, offer) => (Number(offer.price) < Number(best.price) ? offer : best)) : null;
};

// The same part number from other brands, as buyers choose: the original, factory
// quality at a fair price, or the budget option.
function qualityChoices(item) {
  const cheapest = lowestOffer(item.offers);
  const options = [
    { ...item, relation: "SELF", lowest_price: cheapest?.price ?? null, currency: cheapest?.currency, offer_count: (item.offers || []).length },
    ...(item.alternatives || []).filter((alt) => alt.relation === "SAME_NUMBER" && alt.same_variant !== false),
  ];
  const tiers = [
    ["tierBest", (grade) => grade === "ORIGINAL"],
    ["tierBetter", (grade) => grade === "KOREA"],
    ["tierGood", (grade) => !["ORIGINAL", "KOREA"].includes(grade)],
  ];
  const priceKey = (option) => (option.lowest_price != null ? Number(option.lowest_price) : Infinity);
  const picks = tiers.map(([label, test]) => {
    const candidates = options.filter((option) => test(option.quality || "OTHER"));
    if (!candidates.length) return null;
    candidates.sort((a, b) => (priceKey(a) - priceKey(b)) || (b.offer_count - a.offer_count) || ((a.relation === "SELF" ? 0 : 1) - (b.relation === "SELF" ? 0 : 1)));
    return [label, candidates[0]];
  }).filter(Boolean);
  if (picks.length < 2) return null;
  return el("section", { class: "quality-choices" }, [
    el("h3", { text: t("qualityTitle") }),
    el("p", { class: "muted", text: t("qualityLead") }),
    el("div", { class: "quality-grid" }, picks.map(([label, option]) => {
      const self = option.relation === "SELF";
      const price = option.lowest_price != null ? formatPrice(option.lowest_price, option.currency)
        : option.offer_count ? t("offerCount", option.offer_count) : t("priceOnRequest");
      return el(self ? "div" : "button", { class: `quality-option${self ? " is-current" : ""}`, type: self ? null : "button", onclick: self ? null : () => openProduct(option.id) }, [
        el("span", { class: "quality-tier", text: t(label) }),
        qualityBadge(option.quality) || el("span", { class: "quality-badge", text: t("qualityOTHER") }),
        el("strong", { class: "quality-brand", text: brandLabel(option.brand) }),
        el("span", { class: "quality-price", text: price }),
        el("span", { class: "quality-action", text: self ? t("thisPart") : `${t("details")} →` }),
      ]);
    })),
  ]);
}

// ---------- Search filters: quality, brand, order ----------

function renderShopFilters() {
  shopFilters.replaceChildren();
  const data = lastResponse;
  const rows = [];
  const grades = QUALITY_ORDER.filter((grade) => data.quality_counts?.[grade]);
  if (grades.length > 1 || state.quality) {
    rows.push(el("div", { class: "filter-group" }, [
      el("span", { class: "filter-group-label", text: t("filterQuality") }),
      el("div", { class: "pill-row" }, [
        typePill(t("all"), null, !state.quality, () => navigate({ brand: state.brand, quality: "" })),
        ...grades.map((grade) => typePill(t(`quality${grade}`), data.quality_counts[grade], state.quality === grade, () => navigate({ brand: state.brand, quality: grade }))),
      ]),
    ]));
  }
  const brands = data.brand_facets || [];
  if (brands.length > 1 || state.brand) {
    rows.push(el("div", { class: "filter-group" }, [
      el("span", { class: "filter-group-label", text: t("filterBrand") }),
      el("div", { class: "pill-row" }, [
        typePill(t("all"), null, !state.brand, () => navigate({ quality: state.quality, brand: "" })),
        ...brands.slice(0, 10).map((brand) => typePill(CatalogText.brandName(brand) || t("noBrand"), brand.count, state.brand === String(brand.id), () => navigate({ quality: state.quality, brand: brand.id }))),
      ]),
    ]));
  }
  if (data.total > 1) {
    const select = el("select", { "aria-label": t("sortLabel") }, [
      el("option", { value: "", text: t("sortRelevance") }),
      el("option", { value: "price", text: t("sortPrice") }),
    ]);
    select.value = state.sort;
    select.addEventListener("change", () => navigate({ brand: state.brand, quality: state.quality, sort: select.value }));
    rows.push(el("div", { class: "filter-group sort-group" }, [el("span", { class: "filter-group-label", text: t("sortLabel") }), select]));
    enhanceSelect(select);
  }
  shopFilters.append(...rows);
  shopFilters.hidden = !rows.length;
}

// ---------- Favourite sellers ----------

// Mechanics go back to the same stalls; their sellers come first on every part.
let favSellers = new Set(readStored("megaparts_fav_sellers", []));
function toggleFavSeller(id) {
  if (favSellers.has(id)) favSellers.delete(id);
  else favSellers.add(id);
  storage.set("megaparts_fav_sellers", JSON.stringify([...favSellers]));
}

// ---------- Basket ----------

// Parts from several sellers, reserved in one go; each seller gets their own reservations.
const BASKET_KEY = "megaparts_basket";
const MAX_BASKET = 30;
let basket = readStored(BASKET_KEY, []).filter((entry) => entry && Number.isInteger(entry.offer_id));
let basketOffers = new Map();
let sharedList = null;
const inBasket = (offerId) => basket.some((entry) => entry.offer_id === offerId);

function renderBasketButton() {
  const button = $("#basket-button");
  button.querySelector(".basket-count").textContent = basket.length ? String(basket.length) : "";
  button.setAttribute("aria-label", t("basketButton", basket.length));
}

function saveBasket() {
  storage.set(BASKET_KEY, JSON.stringify(basket));
  renderBasketButton();
}

function addToBasket(offerId, productId, quantity = 1) {
  const entry = basket.find((item) => item.offer_id === offerId);
  if (entry) entry.quantity = Math.min(1000, entry.quantity + quantity);
  else if (basket.length < MAX_BASKET) basket.push({ offer_id: offerId, product_id: productId, quantity });
  saveBasket();
}

// The last removal from the basket, so the buyer can take it back with "Undo".
let lastRemoved = null;
function removeFromBasket(offerId, message = null) {
  const index = basket.findIndex((entry) => entry.offer_id === offerId);
  if (index < 0) return;
  const [entry] = basket.splice(index, 1);
  lastRemoved = message ? { entries: [entry], at: index, message } : null;
  saveBasket();
}

function undoRemoval() {
  if (!lastRemoved) return;
  basket.splice(Math.min(lastRemoved.at, basket.length), 0, ...lastRemoved.entries.filter((entry) => !inBasket(entry.offer_id)));
  lastRemoved = null;
  saveBasket();
  renderBasket();
}

// "Add to basket"; once added: open the basket, or take the part out again.
function basketControl(offerId, productId, onChange, onAdd = () => {}) {
  if (!inBasket(offerId)) {
    return el("button", {
      type: "button",
      class: "primary-button basket-add",
      text: t("addToBasket"),
      onclick: () => { addToBasket(offerId, productId); onAdd(); onChange(); },
    });
  }
  return el("div", { class: "basket-added" }, [
    el("span", { class: "basket-added-label", text: t("basketInLabel") }),
    el("button", { type: "button", class: "secondary-button", text: t("basketOpen"), onclick: () => showBasket() }),
    el("button", { type: "button", class: "link-button basket-remove", text: t("basketRemoveFull"), onclick: () => { removeFromBasket(offerId); onChange(); } }),
  ]);
}

const encodeList = (entries) => entries.map((entry) => `${entry.offer_id}:${entry.quantity}`).join(",");
const decodeList = (text) => (text || "").split(",")
  .map((part) => part.split(":").map(Number))
  .filter(([id]) => Number.isInteger(id) && id > 0)
  .map(([id, quantity]) => ({ offer_id: id, quantity: Number.isInteger(quantity) && quantity > 0 ? Math.min(quantity, 1000) : 1 }))
  .slice(0, MAX_BASKET);

async function showBasket(push = true, shared = null) {
  sharedList = shared && shared.length ? shared : null;
  lastRemoved = null;
  if (push) history.pushState(null, "", sharedList ? `/?view=basket&list=${encodeList(sharedList)}` : "/?view=basket");
  showOnly(loading);
  scrollToContent();
  const entries = sharedList || basket;
  try {
    basketOffers = new Map();
    if (entries.length) {
      const response = await fetch(`/api/v1/offers?ids=${entries.map((entry) => entry.offer_id).join(",")}`);
      if (!response.ok) throw new Error(t("searchUnavailable"));
      (await response.json()).forEach((entry) => basketOffers.set(entry.offer.id, entry));
    }
    renderBasket();
  } catch (error) {
    errorBox.textContent = error.message;
    showOnly(errorBox);
  }
}

function basketLine(entry, editable) {
  const data = basketOffers.get(entry.offer_id);
  const remove = () => {
    removeFromBasket(entry.offer_id, t("basketRemoved", data ? productName(data) : t("basketGone")));
    renderBasket();
  };
  const removeButton = editable ? el("button", { type: "button", class: "basket-remove-button", onclick: remove }, [
    el("span", { "aria-hidden": "true", text: "✕" }),
    el("span", { text: t("basketRemove") }),
  ]) : null;
  if (!data) {
    return el("div", { class: "basket-line is-gone" }, [el("span", { text: t("basketGone") }), removeButton]);
  }
  const { offer } = data;
  const setQuantity = (value) => {
    entry.quantity = Math.max(1, Math.min(1000, Math.round(Number(value) || 1)));
    saveBasket();
    renderBasket();
  };
  const quantity = el("input", { type: "number", min: "1", max: "1000", step: "1", value: String(entry.quantity), inputmode: "numeric", "aria-label": t("basketQty"), disabled: !editable });
  quantity.addEventListener("change", () => setQuantity(quantity.value));
  return el("div", { class: "basket-line" }, [
    partThumb(data.category),
    el("div", { class: "basket-line-text" }, [
      el("button", { type: "button", class: "link-button basket-line-name", text: productName(data), onclick: () => openProduct(data.product_id) }),
      el("span", { class: "muted", text: [`${t("brand")}: ${brandLabel(data.brand)}`, data.reference_numbers.slice(0, 2).join(", ")].filter(Boolean).join(" · ") }),
      promoLabel(offer) ? el("span", { class: `offer-promo is-${offer.promo.toLowerCase()}`, text: promoLabel(offer) }) : null,
    ]),
    el("div", { class: "basket-qty" }, [
      el("span", { class: "field-label", text: t("basketQty") }),
      el("div", { class: "qty-stepper" }, [
        el("button", { type: "button", class: "qty-button", "aria-label": t("qtyLess"), text: "−", disabled: !editable || entry.quantity <= 1, onclick: () => setQuantity(entry.quantity - 1) }),
        quantity,
        el("button", { type: "button", class: "qty-button", "aria-label": t("qtyMore"), text: "+", disabled: !editable || entry.quantity >= 1000, onclick: () => setQuantity(entry.quantity + 1) }),
      ]),
    ]),
    el("div", { class: "basket-price" }, [
      el("strong", { text: offer.price != null ? formatPrice(Number(offer.price) * entry.quantity, offer.currency) : t("priceOnRequest") }),
      el("span", { class: `stock stock-${stockSummary([offer]).tone}`, text: stockSummary([offer]).text }),
    ]),
    removeButton,
  ]);
}

function basketShareBox(entries) {
  const link = `${location.origin}/?view=basket&list=${encodeList(entries)}`;
  const text = t("basketShareText", entries.length);
  const copied = el("span", { class: "muted", role: "status" });
  return el("div", { class: "basket-share" }, [
    el("strong", { text: t("basketShare") }),
    el("div", { class: "ask-actions" }, [
      el("a", { class: "secondary-button", href: `https://t.me/share/url?url=${encodeURIComponent(link)}&text=${encodeURIComponent(text)}`, target: "_blank", rel: "noopener", text: t("basketShareTelegram") }),
      el("button", {
        type: "button",
        class: "secondary-button",
        text: t("basketCopy"),
        onclick: async () => {
          try { await navigator.clipboard.writeText(link); copied.textContent = t("basketCopied"); } catch { copied.textContent = link; }
        },
      }),
      copied,
    ]),
  ]);
}

function basketReserveForm(entries) {
  const phone = el("input", { type: "tel", autocomplete: "tel" });
  const vin = el("input", { maxlength: "17", autocomplete: "off", autocapitalize: "characters", spellcheck: "false", value: car.vin || "" });
  const note = el("input", { maxlength: "1000", placeholder: t("reserveNoteHint") });
  const status = el("p", { class: "reserve-status", role: "status" });
  const available = entries.filter((entry) => basketOffers.has(entry.offer_id));
  const formNode = el("form", { class: "reserve-form basket-form" }, [
    field(t("reservePhone"), phone),
    hasCar() ? el("p", { class: "reserve-car" }, [`${t("reserveCar")}: `, el("strong", { text: carLabel() })]) : null,
    field(t("vinLabel"), vin),
    field(t("reserveNote"), note),
    el("button", { type: "submit", class: "primary-button", text: t("basketReserveAll", available.length) }),
    status,
  ]);
  formNode.addEventListener("submit", async (event) => {
    event.preventDefault();
    const vinValue = vin.value.trim().toUpperCase();
    if (vinValue && !VIN_PATTERN.test(vinValue)) {
      status.textContent = t("vinInvalid");
      status.className = "reserve-status is-error";
      return;
    }
    let result = null;
    try {
      const response = await postJson("/api/v1/reservations/basket", {
        session_id: pilotSessionId,
        items: available.map((entry) => ({ product_id: basketOffers.get(entry.offer_id).product_id, supplier_offer_id: entry.offer_id, quantity: entry.quantity })),
        phone: phone.value.trim() || null,
        vehicle_id: car.vehicle_id || null,
        vehicle_label: hasCar() ? carLabel() : null,
        vin: vinValue || null,
        note: note.value.trim() || null,
      });
      if (response.ok) result = await response.json();
    } catch { /* reported below */ }
    if (!result) {
      status.textContent = t("reserveError");
      status.className = "reserve-status is-error";
      return;
    }
    renderBasketSent(result, available, vinValue);
  });
  return formNode;
}

// After reserving: one ready Telegram message per seller with their reservation numbers.
function renderBasketSent(result, entries, vinValue) {
  const bySeller = new Map();
  result.reservations.forEach((reservation) => {
    const data = basketOffers.get(reservation.supplier_offer_id);
    const supplier = data.offer.supplier;
    if (!bySeller.has(supplier.id)) bySeller.set(supplier.id, { supplier, lines: [], ids: [] });
    bySeller.get(supplier.id).lines.push(`№${reservation.id} ${productName(data)} × ${reservation.quantity}`);
    bySeller.get(supplier.id).ids.push(reservation.id);
  });
  basket = basket.filter((entry) => !entries.some((sent) => sent.offer_id === entry.offer_id));
  saveBasket();
  basketView.replaceChildren(
    el("h2", { class: "page-title", text: t("basketTitle") }),
    el("p", { class: "reserve-status is-ok", text: t("basketSent") }),
    el("div", { class: "basket-sent" }, [...bySeller.values()].map(({ supplier, lines, ids }) => {
      const message = t("tgBasket", lines.join("\n"), hasCar() ? carLabel() : t("notGiven"), vinValue || car.vin || t("notGiven"));
      const heading = el("h3", { text: supplierLabel(supplier) });
      const list = el("pre", { class: "basket-lines", text: lines.join("\n") });
      const article = el("article", { class: "basket-seller" });
      // Changed one's mind: cancel this seller's part of the order right here.
      const cancel = cancelControl(t("cancelReservation"), t("cancelConfirm"), async () => {
        const results = await Promise.all(ids.map((id) => postJson(`/api/v1/reservations/${id}/cancel`, { session_id: pilotSessionId })
          .then((response) => response.ok).catch(() => false)));
        if (!results.every(Boolean)) return false;
        article.replaceChildren(heading, list, cancelledNotice(ids.map((id) => ({ id, supplier }))));
        return true;
      });
      article.append(heading, list, el("div", { class: "ask-actions" }, [
        supplier.telegram ? el("a", { class: "primary-button", href: telegramLink(supplier.telegram, message), target: "_blank", rel: "noopener", text: t("messageSeller") }) : null,
        supplier.phone ? el("a", { class: "secondary-button", href: `tel:${supplier.phone}`, text: t("call") }) : null,
        cancel,
      ]));
      return article;
    })),
    el("button", { type: "button", class: "secondary-button", text: t("myReservations"), onclick: () => showReservations() }),
  );
  showOnly(basketView);
}

function renderBasket() {
  const entries = sharedList || basket;
  const editable = !sharedList;
  const groups = new Map();
  entries.forEach((entry) => {
    const data = basketOffers.get(entry.offer_id);
    const key = data ? data.offer.supplier.id : "gone";
    if (!groups.has(key)) groups.set(key, { supplier: data?.offer.supplier, entries: [] });
    groups.get(key).entries.push(entry);
  });
  const totals = new Map();
  let unpriced = false;
  entries.forEach((entry) => {
    const offer = basketOffers.get(entry.offer_id)?.offer;
    if (!offer) return;
    if (offer.price == null) unpriced = true;
    else totals.set(offer.currency, (totals.get(offer.currency) || 0) + Number(offer.price) * entry.quantity);
  });
  const available = entries.filter((entry) => basketOffers.has(entry.offer_id));
  fill(
    basketView,
    el("button", { type: "button", class: "back secondary-button", text: t("back"), onclick: () => (history.length > 1 ? history.back() : showHome()) }),
    el("h2", { class: "page-title", text: editable ? t("basketTitle") : t("sharedListTitle") }),
    editable && lastRemoved ? el("div", { class: "undo-bar", role: "status" }, [
      el("span", { text: lastRemoved.message }),
      el("button", { type: "button", class: "secondary-button", text: t("undo"), onclick: undoRemoval }),
    ]) : null,
    entries.length ? el("p", { class: "muted basket-lead", text: t("basketLead") }) : emptyState(t("basketEmpty")),
    ...[...groups.values()].map(({ supplier, entries: lines }) => el("section", { class: "basket-seller" }, [
      supplier ? el("h3", { text: t("basketSeller", supplierLabel(supplier)) }) : null,
      supplier ? sellerTrust(supplier) : null,
      ...lines.map((entry) => basketLine(entry, editable)),
    ])),
    available.length ? el("div", { class: "basket-summary" }, [
      el("div", { class: "basket-total" }, [
        el("span", { text: t("basketTotal") }),
        el("strong", { text: [...totals.entries()].map(([currency, sum]) => formatPrice(sum, currency)).join(" + ") || "—" }),
      ]),
      unpriced ? el("p", { class: "muted", text: t("basketTotalNote") }) : null,
      editable ? basketReserveForm(entries) : el("button", {
        type: "button",
        class: "primary-button",
        text: t("sharedListAdd"),
        onclick: () => {
          available.forEach((entry) => addToBasket(entry.offer_id, basketOffers.get(entry.offer_id).product_id, entry.quantity));
          showBasket();
        },
      }),
      editable ? basketShareBox(available) : null,
      editable ? el("button", {
        type: "button",
        class: "link-button",
        text: t("basketClear"),
        onclick: () => {
          lastRemoved = { entries: [...basket], at: 0, message: t("basketCleared") };
          basket = [];
          saveBasket();
          renderBasket();
        },
      }) : null,
    ]) : null,
  );
  showOnly(basketView);
}

$("#basket-button").addEventListener("click", () => showBasket());
// Footer and banner links open their page in place, without reloading the site.
document.addEventListener("click", (event) => {
  const link = event.target.closest("[data-view-link]");
  if (!link || event.ctrlKey || event.metaKey || event.shiftKey) return;
  event.preventDefault();
  if (link.dataset.viewLink === "sell") showSell();
  else if (link.dataset.viewLink === "sellers") showSellers();
});

// ---------- Ready repair lists ----------

let jobsCache = { key: null, jobs: [] };
let currentJobId = null;
const carKey = () => JSON.stringify([car.make || "", car.model || "", car.vehicle_id || ""]);
const jobName = (job) => job[`name_${lang}`] || job.name_uz;
const jobPartName = (part) => part[`type_name_${lang}`] || part.type_name_uz;

async function loadJobs() {
  const key = carKey();
  if (jobsCache.key !== key) {
    const response = await fetch(`/api/v1/jobs?${carParams(new URLSearchParams())}`);
    if (!response.ok) throw new Error(t("searchUnavailable"));
    jobsCache = { key, jobs: await response.json() };
  }
  return jobsCache.jobs;
}

async function renderJobCards() {
  const grid = $("#job-grid");
  if (!grid) return;
  let jobs;
  try { jobs = await loadJobs(); } catch { return; }
  $("#jobs-lead").textContent = hasCar() ? t("jobForCar", carLabel()) : t("jobsLead");
  grid.replaceChildren(...jobs.map((job) => {
    const tile = el("button", { type: "button", class: "job-card", onclick: () => showJob(job.id) });
    tile.innerHTML = `<span class="group-icon">${icon(job.icon)}</span><span class="job-text"><span class="job-name"></span><span class="job-count"></span></span>`;
    tile.querySelector(".job-name").textContent = hyphenate(jobName(job));
    tile.querySelector(".job-count").textContent = hasCar() ? `${job.available} / ${job.parts.length}` : t("jobSteps", job.parts.length);
    return tile;
  }));
}

async function showJob(id, push = true) {
  currentJobId = id;
  if (push) history.pushState(null, "", `/?view=job&job=${encodeURIComponent(id)}`);
  showOnly(loading);
  scrollToContent();
  try {
    const job = (await loadJobs()).find((candidate) => candidate.id === id);
    if (!job) throw new Error(t("productNotFound"));
    renderJob(job);
  } catch (error) {
    errorBox.textContent = error.message;
    showOnly(errorBox);
  }
}

function renderJob(job) {
  const picks = job.parts.filter((part) => part.product && (part.product.offers || []).length);
  const status = el("p", { class: "reserve-status is-ok", role: "status" });
  const addAll = el("button", {
    type: "button",
    class: "primary-button",
    text: t("jobAddAll", picks.length),
    onclick: () => {
      picks.forEach((part) => { if (!inBasket(part.product.offers[0].id)) addToBasket(part.product.offers[0].id, part.product.id); });
      status.textContent = t("jobAdded");
      renderJob(job);
    },
  });
  const rows = job.parts.map((part) => {
    const product = part.product;
    const label = [jobPartName(part), part.position ? t(part.position) : null].filter(Boolean).join(" · ");
    if (!product) {
      return el("div", { class: "job-row is-missing" }, [
        el("span", { class: "job-row-type", text: label }),
        el("span", { class: "muted", text: t("jobNone") }),
      ]);
    }
    const offer = product.offers[0];
    const price = priceSummary(product.offers);
    return el("div", { class: "job-row" }, [
      partThumb(product.category),
      el("div", { class: "job-row-text" }, [
        el("span", { class: "job-row-type", text: label }),
        el("button", { type: "button", class: "link-button job-row-name", text: productName(product), onclick: () => openProduct(product.id) }),
        el("span", { class: "result-brand" }, [
          `${t("sellerLabel", sellerNames(product.offers).length)}: `, el("strong", { text: sellerText(product.offers) }),
          ` · ${t("brand")}: `, el("strong", { text: brandLabel(product.brand) }), " ", qualityBadge(product.quality),
        ]),
      ]),
      el("div", { class: "job-row-price" }, [
        el("strong", { text: price.text }),
        el("span", { class: "muted", text: t("offerCount", product.offers.length) }),
      ]),
      el("div", { class: "job-row-actions" }, [
        offer ? basketControl(offer.id, product.id, () => renderJob(job)) : null,
        part.options > 1 ? el("button", { type: "button", class: "link-button", text: t("jobMore", part.options - 1), onclick: () => navigate({ query: "", category: part.type_id }) }) : null,
      ]),
    ]);
  });
  fill(
    jobView,
    el("button", { type: "button", class: "back secondary-button", text: t("back"), onclick: () => showHome() }),
    el("h2", { class: "page-title", text: jobName(job) }),
    hasCar()
      ? el("p", { class: "muted", text: t("jobForCar", carLabel()) })
      : el("div", { class: "fit-verdict is-check" }, [
        el("span", { class: "fit-icon", "aria-hidden": "true", text: "!" }),
        el("div", { class: "fit-text" }, [
          el("strong", { text: t("jobChooseCar") }),
          el("button", { type: "button", class: "link-button", text: t("footerChooseCar"), onclick: openCarPicker }),
        ]),
      ]),
    picks.length ? el("div", { class: "job-actions" }, [addAll, el("button", { type: "button", class: "secondary-button", text: t("basketButton", basket.length), onclick: () => showBasket() }), status]) : null,
    el("div", { class: "job-list" }, rows),
  );
  showOnly(jobView);
}

// ---------- Sellers ----------

async function showSellers(push = true) {
  if (push) history.pushState(null, "", "/?view=sellers");
  showOnly(loading);
  scrollToContent();
  try {
    const response = await fetch("/api/v1/sellers");
    if (!response.ok) throw new Error(t("searchUnavailable"));
    renderSellers(await response.json());
  } catch (error) {
    errorBox.textContent = error.message;
    showOnly(errorBox);
  }
}

let lastSellers = [];
function renderSellers(cards = lastSellers) {
  lastSellers = cards;
  sellersView.replaceChildren(
    el("button", { type: "button", class: "back secondary-button", text: t("back"), onclick: () => showHome() }),
    el("h2", { class: "page-title", text: t("sellersTitle") }),
    el("p", { class: "muted basket-lead", text: t("sellersLead") }),
    el("div", { class: "seller-grid" }, cards.map((card) => {
      const { supplier } = card;
      return el("article", { class: "seller-card" }, [
        el("h3", { text: supplierLabel(supplier) }),
        sellerTrust(supplier),
        el("p", { class: "seller-counts" }, [
          el("strong", { text: t("sellerParts", card.active_offers_count) }),
          card.priced_offers_count ? ` · ${t("sellerPriced", card.priced_offers_count)}` : "",
        ]),
        card.brands.length ? el("p", { class: "seller-brands" }, [el("span", { class: "meta-label", text: t("brand") }), ` ${card.brands.join(", ")}`]) : null,
        card.last_data_update ? el("p", { class: "muted seller-date", text: t("sellerLastList", formatDate(card.last_data_update)) }) : null,
        el("div", { class: "ask-actions" }, [
          el("a", { class: "primary-button", href: `/suppliers/${supplier.id}`, text: t("sellerOpen") }),
          supplier.telegram ? el("a", { class: "secondary-button", href: telegramLink(supplier.telegram), target: "_blank", rel: "noopener", text: "Telegram" }) : null,
          supplier.phone ? el("a", { class: "secondary-button", href: `tel:${supplier.phone}`, text: t("call") }) : null,
        ]),
      ]);
    })),
  );
  showOnly(sellersView);
}

// ---------- Sell on MegaParts ----------

function showSell(push = true) {
  if (push) history.pushState(null, "", "/?view=sell");
  const inputs = {
    business_name: el("input", { required: true, minlength: "2", maxlength: "200", autocomplete: "organization" }),
    contact_name: el("input", { maxlength: "200", autocomplete: "name" }),
    phone: el("input", { required: true, minlength: "7", maxlength: "50", type: "tel", autocomplete: "tel" }),
    telegram: el("input", { maxlength: "100" }),
    city: el("input", { maxlength: "200", autocomplete: "address-level2" }),
    address: el("input", { maxlength: "500" }),
    cars: el("input", { maxlength: "300", placeholder: "Nexia, Cobalt, Damas…" }),
    note: el("input", { maxlength: "1000" }),
  };
  const labels = { business_name: "sellBusiness", contact_name: "sellContact", phone: "sellPhone", telegram: "sellTelegram", city: "sellCity", address: "sellAddress", cars: "sellCars", note: "sellNote" };
  const status = el("p", { class: "reserve-status", role: "status" });
  const formNode = el("form", { class: "request-form sell-form" }, [
    ...Object.entries(inputs).map(([key, node]) => field(t(labels[key]), node)),
    el("button", { type: "submit", class: "primary-button", text: t("sellSend") }),
    status,
  ]);
  formNode.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = Object.fromEntries(Object.entries(inputs).map(([key, node]) => [key, node.value.trim() || null]));
    let ok = false;
    try { ok = (await postJson("/api/v1/seller-applications", payload)).ok; } catch { /* reported below */ }
    status.textContent = ok ? t("sellSent") : t("reserveError");
    status.className = `reserve-status ${ok ? "is-ok" : "is-error"}`;
    if (ok) formNode.querySelectorAll("input, button").forEach((node) => { node.disabled = true; });
  });
  sellView.replaceChildren(
    el("button", { type: "button", class: "back secondary-button", text: t("back"), onclick: () => showHome() }),
    el("div", { class: "sell-intro" }, [
      el("h2", { class: "page-title", text: t("sellTitle") }),
      el("p", { class: "hero-lead-dark", text: t("sellLead") }),
      el("ul", { class: "sell-points" }, t("sellPoints").map((point) => el("li", { text: point }))),
    ]),
    formNode,
  );
  showOnly(sellView);
  scrollToContent();
}

// ---------- Questions ----------

function renderFaq() {
  const list = $("#faq-list");
  if (!list) return;
  list.replaceChildren(...t("faq").map(([question, answer]) => el("details", { class: "faq-item" }, [
    el("summary", { text: question }),
    el("p", { text: answer }),
  ])));
}

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

// ---------- Language and page wiring ----------

function renderExamples() {
  $("#example-list").replaceChildren(...t("exampleQueries").map((query) => el("button", {
    type: "button",
    class: "example",
    lang,
    text: query,
    onclick: () => navigate({ query, category: "" }),
  })));
}

// The empty search box types out real examples, so it is clear what can be searched for.
let placeholderTimer = 0;
function typeExamples() {
  clearTimeout(placeholderTimer);
  const plain = t("searchPlaceholder");
  input.placeholder = plain;
  if (reducedMotion) return;
  const words = t("exampleQueries");
  let word = 0;
  let shown = 0;
  let erasing = false;
  const tick = () => {
    if (document.activeElement === input || input.value) {
      input.placeholder = plain;
      placeholderTimer = setTimeout(tick, 1500);
      return;
    }
    const text = words[word % words.length];
    shown += erasing ? -1 : 1;
    input.placeholder = `${t("examples")} ${text.slice(0, shown)}`;
    let delay = erasing ? 30 : 75;
    if (!erasing && shown >= text.length) { erasing = true; delay = 1800; }
    else if (erasing && shown <= 0) { erasing = false; word += 1; delay = 450; }
    placeholderTimer = setTimeout(tick, delay);
  };
  placeholderTimer = setTimeout(tick, 900);
}

function applyLanguage() {
  document.documentElement.lang = lang;
  document.title = t("pageTitle");
  document.querySelectorAll("[data-i18n]").forEach((node) => { node.textContent = t(node.dataset.i18n); });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => { node.placeholder = t(node.dataset.i18nPlaceholder); });
  document.querySelectorAll("[data-i18n-aria]").forEach((node) => { node.setAttribute("aria-label", t(node.dataset.i18nAria)); });
  document.querySelectorAll("[data-lang]").forEach((button) => { button.setAttribute("aria-pressed", String(button.dataset.lang === lang)); });
  renderExamples();
  typeExamples();
  renderGarage();
  renderGroups();
  if (!resultsView.hidden && lastResponse) renderResults();
  if (!detailView.hidden && lastDetail) renderDetail();
  if (!reservationsView.hidden) renderReservations();
  renderBasketButton();
  renderFaq();
  if (!basketView.hidden && basketView.querySelector(".basket-summary, .basket-lead")) renderBasket();
  if (!jobView.hidden && currentJobId) showJob(currentJobId, false);
  if (!sellersView.hidden) renderSellers();
  if (!sellView.hidden) showSell(false);
}

document.querySelectorAll("[data-lang]").forEach((button) => button.addEventListener("click", () => {
  lang = button.dataset.lang;
  storage.set("megaparts_lang", lang);
  closeSuggestions();
  applyLanguage();
}));

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
  state.brand = params.get("brand") || "";
  state.quality = params.get("quality") || "";
  state.sort = params.get("sort") || "";
  input.value = state.query;
  // /part/{id}; ?product= links from before part pages had their own address still work.
  const partPath = location.pathname.match(/^\/part\/([^/]+)$/);
  const product = partPath ? decodeURIComponent(partPath[1]) : params.get("product");
  const view = params.get("view");
  if (product) openProduct(product, false);
  else if (view === "reservations") showReservations(false);
  else if (view === "basket") showBasket(false, params.get("list") ? decodeList(params.get("list")) : null);
  else if (view === "job" && params.get("job")) showJob(params.get("job"), false);
  else if (view === "sellers") showSellers(false);
  else if (view === "sell") showSell(false);
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
