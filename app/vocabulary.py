"""Search vocabulary assembled per request: static synonyms, admin aliases, and catalog words.

The catalog is small (hundreds of products), so the lexicon is rebuilt on every search.
That keeps admin alias changes and catalog re-imports effective immediately.
"""

from __future__ import annotations

import re
from bisect import bisect_left
from collections import Counter
from dataclasses import dataclass, field
from itertools import product

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Brand, Category, Product, SearchAlias, SearchSynonym, Vehicle
from app.normalization import normalize_text, sanitize_query, tokenize
from app.search_vocabulary import (
    POSITION_SYNONYMS,
    PRODUCT_SYNONYMS,
    RELATED_PRODUCT_MARKERS,
    SIDE_SYNONYMS,
    STOP_WORDS,
    VEHICLE_ALIASES,
)

MIN_CORRECTABLE_LENGTH = 3
# A misspelled start of a longer word ("salnek" for "salniklari") needs some letters to go on.
MIN_PREFIX_CORRECTION_LENGTH = 5
MIN_SPLIT_PART = 3
# Each search tries at most this many corrected queries, from this many choices per word.
MAX_TOKEN_OPTIONS = 3
MAX_QUERY_OPTIONS = 6
# Shorter catalog model names (K5, X70, Han) are too ambiguous to recognize alone.
MIN_AUTO_MODEL_ALIAS_LENGTH = 4

# Letters people swap when spelling by ear: Uzbek h/x and q/k, transliteration (ks/x, iy/i,
# c/k), unstressed о/а and е/и, voiced/voiceless pairs (kalotka/kolodka), soft signs, and
# doubled letters. Words with the same key sound alike, so "neksiya" reaches "nexia".
_PHONETIC_STEPS = (
    ("ch", "ç"), ("sh", "ş"), ("kh", "x"), ("ks", "x"), ("h", "x"), ("c", "k"), ("q", "k"),
    ("w", "v"), ("iy", "i"), ("y", "i"), ("o", "a"), ("e", "i"),
    ("d", "t"), ("g", "k"), ("b", "p"), ("z", "s"),
    ("о", "а"), ("э", "и"), ("е", "и"), ("ы", "и"), ("й", "и"), ("щ", "ш"), ("ь", ""), ("ъ", ""),
    ("д", "т"), ("г", "к"), ("б", "п"), ("з", "с"),
)
_DOUBLED = re.compile(r"(.)\1+")

# The same physical keys on the English (QWERTY) and Russian (ЙЦУКЕН) layouts.
_LATIN_KEYS = "`qwertyuiop[]asdfghjkl;'zxcvbnm,."
_CYRILLIC_KEYS = "ёйцукенгшщзхъфывапролджэячсмитьбю"
_TO_CYRILLIC = str.maketrans(_LATIN_KEYS, _CYRILLIC_KEYS)
_TO_LATIN = str.maketrans(_CYRILLIC_KEYS, _LATIN_KEYS)


def phonetic_key(word: str) -> str:
    for old, new in _PHONETIC_STEPS:
        word = word.replace(old, new)
    return _DOUBLED.sub(r"\1", word)


@dataclass
class SearchVocabulary:
    product_synonyms: dict[str, tuple[str, ...]]
    vehicle_aliases: dict[str, tuple[str, ...]]
    brand_names: list[str]
    word_counts: Counter[str] = field(default_factory=Counter)
    sorted_words: list[str] = field(default_factory=list)
    phonetic_keys: dict[str, str] = field(default_factory=dict)
    # Sound key -> the proper spelling: the catalog's own, else the first-listed synonym.
    # Synonym lists also hold common misspellings ("amartizator"); they match fine, but
    # the fix shown should be "amortizator".
    catalog_spellings: dict[str, str] = field(default_factory=dict)
    # Category id -> its uz/ru/en names and its group's, so "шрус" finds CV joints.
    category_texts: dict[str, str] = field(default_factory=dict)

    def is_known(self, token: str) -> bool:
        if token in self.word_counts or token in STOP_WORDS:
            return True
        # Prefixes are matched by substring search, so they are not misspellings.
        index = bisect_left(self.sorted_words, token)
        return index < len(self.sorted_words) and self.sorted_words[index].startswith(token)


def merge_aliases(
    base: dict[str, tuple[str, ...]], aliases: list[tuple[str, str]]
) -> dict[str, tuple[str, ...]]:
    merged = dict(base)
    for canonical, alias in aliases:
        existing = merged.get(canonical, (canonical,))
        merged[canonical] = tuple(dict.fromkeys((*existing, alias)))
    return merged


def _words(value: str | None) -> set[str]:
    # Both spellings count: the typed one ("oldi") and its canonical form ("front").
    return {
        token
        for token in (*tokenize(value), *normalize_text(value).split())
        if len(token) >= 3 and not any(char.isdigit() for char in token)
    }


def catalog_vehicle_aliases(
    session: Session, static: dict[str, tuple[str, ...]]
) -> list[tuple[str, str]]:
    """Recognize every catalog model by name, e.g. "nexia" -> "Daewoo Nexia"."""
    known = {normalize_text(alias) for aliases in static.values() for alias in aliases}
    pairs: list[tuple[str, str]] = []
    for make, model in session.execute(select(Vehicle.make, Vehicle.model).distinct()):
        model_key = normalize_text(model)
        if (
            model.startswith("(")
            or len(model_key) < MIN_AUTO_MODEL_ALIAS_LENGTH
            or not any(char.isalpha() for char in model_key)
        ):
            continue
        canonical = " ".join(filter(None, [make, model]))
        if canonical in static:
            continue
        for alias in (normalize_text(canonical), model_key):
            if alias not in known:
                pairs.append((canonical, alias))
    return pairs


def workbook_vehicle_synonyms(session: Session) -> list[tuple[str, str]]:
    """Workbook "Search Synonyms" for vehicles, e.g. "Нексия 1" -> "Daewoo Nexia"."""
    rows = session.execute(
        select(Vehicle.make, Vehicle.model, SearchSynonym.term)
        .join(Vehicle, Vehicle.id == SearchSynonym.target_id)
        .where(SearchSynonym.target_type == "VEHICLE")
    ).all()
    return [
        (" ".join(filter(None, [make, model])), normalize_text(term))
        for make, model, term in rows
        if not model.startswith("(") and len(normalize_text(term)) >= 3
    ]


def load_vocabulary(session: Session) -> SearchVocabulary:
    aliases = session.execute(
        select(SearchAlias.kind, SearchAlias.canonical, SearchAlias.alias)
    ).all()
    product_synonyms = merge_aliases(
        PRODUCT_SYNONYMS,
        [(canonical, alias) for kind, canonical, alias in aliases if kind == "product"],
    )
    vehicle_aliases = merge_aliases(
        VEHICLE_ALIASES,
        [
            *catalog_vehicle_aliases(session, VEHICLE_ALIASES),
            *workbook_vehicle_synonyms(session),
            *((canonical, alias) for kind, canonical, alias in aliases if kind == "vehicle"),
        ],
    )
    brand_names = list(session.scalars(select(Brand.name)).all())

    counts: Counter[str] = Counter()
    names = list(session.scalars(select(Product.normalized_name).where(Product.is_searchable)))
    for name in names:
        counts.update(_words(name))
    for text in session.scalars(select(Vehicle.normalized_text)):
        counts.update(_words(text))
    for name in brand_names:
        counts.update(_words(name))
    categories = {category.id: category for category in session.scalars(select(Category))}
    category_texts: dict[str, str] = {}
    for category in categories.values():
        own = [category.name_uz, category.name_ru, category.name_en]
        counts.update(_words(" ".join(filter(None, own))))
        parent = categories.get(category.parent_id)
        group = [parent.name_uz, parent.name_ru, parent.name_en] if parent else []
        category_texts[category.id] = normalize_text(" ".join(filter(None, own + group)))
    catalog_spellings: dict[str, str] = {}
    for word, _count in counts.most_common():
        catalog_spellings.setdefault(phonetic_key(word), word)
    # A synonym is as common as the parts it finds: "kolodka" leads to every brake pad.
    for aliases in product_synonyms.values():
        expansions = [normalize_text(alias) for alias in aliases]
        found = sum(1 for name in names if any(expansion in name for expansion in expansions))
        for alias in aliases:
            words = _words(alias)
            counts.update(dict.fromkeys(words, found))
            # Proper spellings are listed before misspellings ("kolodka", "kalodka").
            for word in sorted(words):
                catalog_spellings.setdefault(phonetic_key(word), word)
    for group in (
        product_synonyms,
        vehicle_aliases,
        POSITION_SYNONYMS,
        SIDE_SYNONYMS,
        RELATED_PRODUCT_MARKERS,
    ):
        for canonical, values in group.items():
            for value in (canonical, *values):
                counts.update(_words(value))

    return SearchVocabulary(
        product_synonyms=product_synonyms,
        vehicle_aliases=vehicle_aliases,
        brand_names=brand_names,
        word_counts=counts,
        sorted_words=sorted(counts),
        phonetic_keys={word: phonetic_key(word) for word in counts},
        catalog_spellings=catalog_spellings,
        category_texts=category_texts,
    )


def edit_distance(left: str, right: str, limit: int) -> int:
    """Optimal string alignment distance; returns limit + 1 once it is exceeded."""
    if abs(len(left) - len(right)) > limit:
        return limit + 1
    previous_previous: list[int] = []
    previous = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current = [i] + [0] * len(right)
        for j, right_char in enumerate(right, start=1):
            cost = left_char != right_char
            current[j] = min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + cost)
            if (
                i > 1
                and j > 1
                and left_char == right[j - 2]
                and left[i - 2] == right_char
            ):
                current[j] = min(current[j], previous_previous[j - 2] + 1)
        if min(current) > limit:
            return limit + 1
        previous_previous, previous = previous, current
    return previous[-1]


def _split_joined(token: str, vocabulary: SearchVocabulary) -> str | None:
    """Words typed without a space: "moyfiltri" -> "moy filtri"."""
    best: tuple[int, str] | None = None
    for index in range(MIN_SPLIT_PART, len(token) - MIN_SPLIT_PART + 1):
        left, right = token[:index], token[index:]
        if left in vocabulary.word_counts and vocabulary.is_known(right):
            score = vocabulary.word_counts[left] + vocabulary.word_counts.get(right, 0)
            if best is None or score > best[0]:
                best = (score, f"{left} {right}")
    return best[1] if best else None


def _prefix_distance(token: str, word: str, limit: int) -> int:
    """Distance from the token to the closest start of a longer word."""
    sizes = range(max(MIN_CORRECTABLE_LENGTH, len(token) - 1), min(len(word), len(token) + 1) + 1)
    return min((edit_distance(token, word[:size], limit) for size in sizes), default=limit + 1)


def _token_options(token: str, vocabulary: SearchVocabulary) -> list[str]:
    """Likely intended words for a misspelled token, best first; empty when it is fine."""
    if (
        len(token) < MIN_CORRECTABLE_LENGTH
        or any(char.isdigit() for char in token)
        or vocabulary.is_known(token)
    ):
        return []
    if len(token) >= 2 * MIN_SPLIT_PART and (split := _split_joined(token, vocabulary)):
        return [split]
    limit = 1 if len(token) <= 5 else 2
    key = phonetic_key(token)
    ranked: list[tuple[int, bool, int, int, str]] = []
    for word, count in vocabulary.word_counts.items():
        spelled = edit_distance(token, word, limit)
        distance = min(spelled, edit_distance(key, vocabulary.phonetic_keys[word], limit))
        partial = False
        if (
            distance > limit
            and len(token) >= MIN_PREFIX_CORRECTION_LENGTH
            and len(word) > len(token)
        ):
            # Search matches inside words, so fixing the start of a longer word is enough.
            distance = spelled = _prefix_distance(token, word, limit)
            partial = True
        if distance > limit:
            continue
        # Whole words beat partial ones, a real spelling slip beats a sound-alike,
        # and words that lead to more parts beat rare ones.
        ranked.append((distance, partial, spelled, -count, word))
    words = [entry[-1] for entry in sorted(ranked)]
    return list(dict.fromkeys(_proper_spelling(word, vocabulary) for word in words))[
        :MAX_TOKEN_OPTIONS
    ]


def _proper_spelling(word: str, vocabulary: SearchVocabulary) -> str:
    """"amartizator" -> "amortizator": a listed misspelling one letter off the real word."""
    spelling = vocabulary.catalog_spellings.get(vocabulary.phonetic_keys[word], word)
    # Sound keys are coarse ("pad" and "boot" share one), so only near-identical words swap.
    return spelling if edit_distance(word, spelling, 1) <= 1 else word


def correction_options(query: str, vocabulary: SearchVocabulary) -> list[str]:
    """Corrected versions of the query, most likely first; empty when nothing changed."""
    tokens = tokenize(query)
    options = [_token_options(token, vocabulary) or [token] for token in tokens]
    if all(choice == [token] for choice, token in zip(options, tokens, strict=True)):
        return []
    # Fewest second-choice words first.
    combinations = sorted(product(*(range(len(choice)) for choice in options)), key=sum)
    return [
        " ".join(choice[index] for choice, index in zip(options, combination, strict=True))
        for combination in combinations[:MAX_QUERY_OPTIONS]
    ]


def correct_query(query: str, vocabulary: SearchVocabulary) -> str | None:
    """Return the query with misspelled tokens replaced, or None when nothing changed."""
    options = correction_options(query, vocabulary)
    return options[0] if options else None


def _swap_layout(text: str) -> str | None:
    letters = [char for char in text if char.isalpha()]
    if letters and all(char in _CYRILLIC_KEYS for char in letters):
        return text.translate(_TO_LATIN)
    if letters and all("a" <= char <= "z" for char in letters):
        return text.translate(_TO_CYRILLIC)
    return None


def swap_keyboard_layout(query: str, vocabulary: SearchVocabulary) -> str | None:
    """Words typed with the wrong keyboard layout: "cdtxf" -> "свеча", "ымусрф" -> "svecha".

    Only words the catalog does not know are swapped, and only when the swapped word is
    one it knows (or nearly), so "cobalt cdtxf" becomes "cobalt свеча".
    """
    words = query.casefold().split()
    swapped_any = False
    result = []
    for word in words:
        tokens = tokenize(word)
        swapped = _swap_layout(word)
        swapped_tokens = tokenize(swapped) if swapped else []
        if (
            tokens
            and not all(vocabulary.is_known(token) or token.isdigit() for token in tokens)
            and swapped_tokens
            and all(
                vocabulary.is_known(token) or _token_options(token, vocabulary)
                for token in swapped_tokens
            )
        ):
            result.append(swapped)
            swapped_any = True
        else:
            result.append(word)
    return " ".join(result) if swapped_any else None


def correction_candidates(query: str, vocabulary: SearchVocabulary) -> list[str]:
    """Rewrites of a query that found nothing good, most likely first.

    Search tries them in order and keeps the first that finds parts, so a plausible but
    useless fix ("brake pro") gives way to the next one ("brake pad").
    """
    candidates = correction_options(sanitize_query(query), vocabulary)
    # The layout swap reads the raw text: "," and ";" are the Russian "б" and "ж" keys.
    swapped = swap_keyboard_layout(query, vocabulary)
    if swapped:
        cleaned = sanitize_query(swapped)
        candidates += correction_options(cleaned, vocabulary) or [cleaned]
    return list(dict.fromkeys(candidates))


def without_unknown_words(query: str, vocabulary: SearchVocabulary) -> str | None:
    """The query minus words the catalog has never seen ("колодки для моей ласточки").

    A last resort, since it drops what the customer typed. Judged on the words as typed:
    a stray word "corrected" into some catalog word would otherwise stay.
    """
    words = [token for token in tokenize(sanitize_query(query)) if token not in STOP_WORDS]
    known = [
        token
        for token in words
        if vocabulary.is_known(token) or any(char.isdigit() for char in token)
    ]
    return " ".join(known) if known and len(known) < len(words) else None
