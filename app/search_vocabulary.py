"""Centralized query-expansion vocabulary; catalog values are never rewritten."""

PRODUCT_SYNONYMS: dict[str, tuple[str, ...]] = {
    "spark plug": ("spark plug", "свеча", "svecha"),
    "shock absorber": ("амортизатор", "амартизатор", "amortizator", "amartizator"),
    "fuel pump": ("бензонасос", "бензин насос", "benzin nasos", "fuel pump"),
    "ignition coil": ("катушка", "babina", "ignition coil"),
    "brake pad": ("колодка", "kolodka", "kalodka", "brake pad"),
    "sensor": ("датчик", "datchik", "dachchik", "sensor"),
    "abs": ("abs", "abc"),
}

# A product phrase can occur in an accessory name (for example, shock-absorber
# bushing). These markers keep accessories discoverable under RELATED without
# mixing them into exact part results.
RELATED_PRODUCT_MARKERS: dict[str, tuple[str, ...]] = {
    "spark plug": ("pravoda", "pravada", "провод", "wire"),
    "shock absorber": (
        "втулка",
        "чашка",
        "резина",
        "rezina",
        "пыльник",
        "pilnik",
        "опора",
        "podushka",
        "support",
    ),
}

POSITION_SYNONYMS: dict[str, tuple[str, ...]] = {
    "front": ("front", "oldi", "oldingi", "передний", "передняя", "передн", "peredniy"),
    "rear": ("rear", "orqa", "задний", "задняя", "задн", "zadniy"),
}

SIDE_SYNONYMS: dict[str, tuple[str, ...]] = {
    "left": ("left", "lh", "chap", "левый", "левая", "лев", "lev", "leviy"),
    "right": (
        "right",
        "rh",
        "o'ng",
        "ong",
        "правый",
        "правая",
        "прав",
        "prav",
        "praviy",
    ),
}

# Filler words people type in a sentence ("Cobalt uchun svecha kerak", "нужны колодки
# для нексии"). They are dropped from the part being searched and never spell-corrected.
STOP_WORDS: frozenset[str] = frozenset({
    # Uzbek
    "kerak", "kerakli", "kerakmi", "uchun", "menga", "bormi", "bor", "narxi", "narx",
    "qancha", "nechpul", "necha", "sotib", "olish", "olaman", "olmoqchiman", "va", "bilan",
    "ham", "mashina", "mashinaga", "mashinam", "mashinamga", "avto", "avtomobil", "detal",
    "detali", "detallar", "zapchast", "zapchasti", "ehtiyot", "qism", "qismi", "yangi",
    "iltimos", "salom",
    # Russian
    "для", "на", "нужен", "нужна", "нужно", "нужны", "надо", "купить", "куплю", "цена",
    "цены", "сколько", "стоит", "есть", "ли", "мне", "машина", "машину", "машины", "авто",
    "автомобиль", "запчасть", "запчасти", "деталь", "детали", "новый", "новая", "новые",
    "пожалуйста", "здравствуйте",
    # English
    "for", "need", "needs", "the", "an", "my", "car", "buy", "price", "part", "parts", "to",
    "of", "and", "with", "please", "new",
})

# Ravon is the 2016–2020 export badge for the same Uzbek-built cars.
VEHICLE_ALIASES: dict[str, tuple[str, ...]] = {
    "Chevrolet Cobalt": ("cobalt", "chevrolet cobalt", "kobalt", "ravon r4"),
    "Chevrolet Nexia 3": (
        "nexia3",
        "nexia 3",
        "nexia-3",
        "ravon r3",
        "ravon nexia",
        "ravon nexia r3",
    ),
    "Chevrolet Tracker 2": ("tracker2", "tracker 2", "tracker ii", "chevrolet tracker 2"),
    "Chevrolet Spark": ("chevrolet spark", "spark", "ravon r2"),
    "Chevrolet Damas": ("chevrolet damas", "damas"),
    "Chevrolet Matiz": ("chevrolet matiz", "matiz", "ravon matiz"),
    "Chevrolet Lacetti": ("chevrolet lacetti", "lacetti", "lasetti"),
    "Chevrolet Gentra": ("chevrolet gentra", "gentra", "ravon gentra"),
    "Chevrolet Malibu": ("chevrolet malibu", "malibu"),
    "Chevrolet Orlando": ("chevrolet orlando", "orlando"),
    "Chevrolet Captiva": ("chevrolet captiva", "captiva"),
    "Chevrolet Onix": ("chevrolet onix", "onix"),
    "Chevrolet Monza": ("chevrolet monza", "monza"),
    "Chevrolet Epica": ("chevrolet epica", "epica"),
}
