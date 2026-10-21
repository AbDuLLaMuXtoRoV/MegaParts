import re
import unicodedata

from app.search_vocabulary import POSITION_SYNONYMS, SIDE_SYNONYMS

_NON_WORD = re.compile(r"[_\W]+", flags=re.UNICODE)
_NON_ALNUM = re.compile(r"[^0-9a-zа-яё]+", flags=re.IGNORECASE)
# Uzbek o‘/g‘ are written with any of these marks, or with none at all ("ot", "yoqilgi").
_APOSTROPHES = re.compile(r"['`´‘’ʻʼ]")


def _base(value: object | None) -> str:
    if value is None:
        return ""
    return unicodedata.normalize("NFKC", str(value)).casefold().strip()


def tokenize(value: object | None) -> list[str]:
    """Split into casefolded word tokens without canonicalizing position/side aliases."""
    text = _APOSTROPHES.sub("", _base(value)).replace("ё", "е")
    return _NON_WORD.sub(" ", text).split()


TOKEN_ALIASES = {
    token: canonical
    for groups in (POSITION_SYNONYMS, SIDE_SYNONYMS)
    for canonical, aliases in groups.items()
    for alias in aliases
    for token in tokenize(alias)
}
TOKEN_ALIASES["orqа"] = "rear"  # final character is Cyrillic in some exports


def normalize_text(value: object | None) -> str:
    return " ".join(TOKEN_ALIASES.get(token, token) for token in tokenize(value))


# Uzbek Cyrillic to the Latin alphabet the catalog is written in ("колодкалари" -> "kolodkalari").
_UZBEK_LATIN = str.maketrans({
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ж": "j", "з": "z", "и": "i",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s",
    "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
    "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "o", "қ": "q", "ғ": "g",
    "ҳ": "h",
})


def uzbek_latin(text: str) -> str:
    return text.translate(_UZBEK_LATIN)


def normalize_code(value: object | None) -> str:
    return _NON_ALNUM.sub("", _base(value))


def sanitize_query(value: object | None) -> str:
    """Remove accidental separators while retaining the untouched query separately."""
    unquoted = _APOSTROPHES.sub("", _base(value))
    cleaned = " ".join(re.sub(r"""[\\/,;"“”]+""", " ", unquoted).split())
    return re.sub(r"[.!?…:|\-]+$", "", cleaned).strip()


def query_tokens(value: str) -> list[str]:
    return list(dict.fromkeys(normalize_text(value).split()))
