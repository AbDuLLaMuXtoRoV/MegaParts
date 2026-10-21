import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.catalog import refresh_products
from app.database import get_session
from app.main import app, settings
from app.models import Base, Category, Fitment, Product, SearchEvent, SearchSynonym, Vehicle
from app.normalization import normalize_text
from app.search import search_products
from app.vocabulary import (
    correction_options,
    load_vocabulary,
    phonetic_key,
    swap_keyboard_layout,
)

CATEGORIES = [
    ("CAT-IGN", None, "O't oldirish tizimi", "Система зажигания", "Ignition system"),
    ("CAT-IGN-PLUG", "CAT-IGN", "O't oldirish shamlari (svecha)", "Свечи зажигания", "Spark plugs"),
    ("CAT-IGN-COIL", "CAT-IGN", "O't oldirish g'altagi (babina)", "Катушка зажигания (бабина)",
     "Ignition coil"),
    ("CAT-FLT", None, "Filtrlar", "Фильтры", "Filters"),
    ("CAT-FLT-OIL", "CAT-FLT", "Moy filtri", "Фильтр масляный", "Oil filter"),
    ("CAT-FLT-FUEL", "CAT-FLT", "Yoqilg'i filtri", "Фильтр топливный", "Fuel filter"),
    ("CAT-BRK", None, "Tormoz tizimi", "Тормозная система", "Braking"),
    ("CAT-BRK-PAD", "CAT-BRK", "Tormoz kolodkalari", "Колодки тормозные", "Brake pads"),
    ("CAT-SUS", None, "Osma", "Подвеска", "Suspension"),
    ("CAT-SUS-SHOCK", "CAT-SUS", "Amortizator", "Амортизатор", "Shock absorber"),
    ("CAT-ENG", None, "Dvigatel", "Двигатель", "Engine"),
    ("CAT-ENG-VSEAL", "CAT-ENG", "Klapan salniklari", "Маслосъёмные колпачки", "Valve stem seals"),
    ("CAT-ENG-HEAD", "CAT-ENG", "Silindrlar kallagi (golovka)", "Головка блока цилиндров",
     "Cylinder head"),
]

PRODUCTS = [
    ("PLUG", "O't oldirish shamlari (svecha)", "Свечи зажигания", "Spark plug", "CAT-IGN-PLUG", "COB"),
    ("COIL", "O't oldirish g'altagi (babina)", "Бабина", "Ignition coil", "CAT-IGN-COIL", "COB"),
    ("OIL", "Moy filtri", "Фильтр масляный", "Oil filter", "CAT-FLT-OIL", "COB"),
    ("FUEL", "Yoqilgʻi filtri", "Фильтр топливный", "Fuel filter", "CAT-FLT-FUEL", "COB"),
    ("PAD", "Tormoz kolodkalari old", "Колодки тормозные", "Brake pad", "CAT-BRK-PAD", "COB"),
    ("SHOCK", "Amortizator orqa", "Амортизатор задний", "Shock absorber", "CAT-SUS-SHOCK", "NEX"),
    ("SEAL", "Klapan salniklari", "Маслосъёмные колпачки", "Valve stem seals", "CAT-ENG-VSEAL",
     "COB"),
    ("HEAD", "Silindrlar kallagi", "Головка блока цилиндров", "Cylinder head", "CAT-ENG-HEAD",
     "COB"),
]


def make_engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for category_id, parent_id, name_uz, name_ru, name_en in CATEGORIES:
            session.add(
                Category(
                    id=category_id,
                    parent_id=parent_id,
                    name_uz=name_uz,
                    name_ru=name_ru,
                    name_en=name_en,
                    is_leaf=parent_id is not None,
                )
            )
        vehicles = {
            "COB": Vehicle(
                id="COB", make="Chevrolet", model="Cobalt", normalized_text="chevrolet cobalt"
            ),
            "NEX": Vehicle(id="NEX", make="Daewoo", model="Nexia", normalized_text="daewoo nexia"),
        }
        # As in the workbook's Search Synonyms sheet.
        session.add(SearchSynonym(id="SYN-1", target_type="VEHICLE", target_id="COB", term="Кобальт"))
        for product_id, name, name_ru, name_en, category_id, vehicle_id in PRODUCTS:
            product = Product(
                id=product_id,
                name=name,
                name_ru=name_ru,
                name_en=name_en,
                normalized_name="",
                category_id=category_id,
                audit_status="CONFIRMED",
                is_searchable=True,
            )
            product.fitments.append(Fitment(vehicle=vehicles[vehicle_id]))
            session.add(product)
        session.flush()
        refresh_products(session)
        session.commit()
    return engine


@pytest.fixture
def session():
    with Session(make_engine()) as session:
        yield session


def test_uzbek_apostrophes_in_any_form_or_none_read_the_same() -> None:
    spellings = ["Yoqilg'i", "yoqilgʻi", "yoqilg‘i", "yoqilg`i", "yoqilgi"]
    assert {normalize_text(spelling) for spelling in spellings} == {"yoqilgi"}
    assert normalize_text("o'ng") == "right"
    assert normalize_text("ёлка") == "елка"


def test_sound_alike_spellings_share_a_key() -> None:
    assert phonetic_key("neksiya") == phonetic_key("nexia")
    assert phonetic_key("амартизатор") == phonetic_key("амортизатор")
    assert phonetic_key("xavo") == phonetic_key("havo")


@pytest.mark.parametrize(
    ("typed", "expected_id", "corrected"),
    [
        # Typing slips, sound-alike spellings and a misspelled start of a longer word.
        ("svica", "PLUG", "svecha"),
        ("amartizatr", "SHOCK", "amortizator"),
        ("neksiya amortizator", "SHOCK", "nexia amortizator"),
        ("salnek", "SEAL", "salniklari"),
        ("brake pda", "PAD", "brake pad"),
        ("калодки", "PAD", "колодки"),
        # Spelled by ear; brake pads, not the similar-looking "kallagi" (cylinder head).
        ("kalotki", "PAD", "kolodka"),
        # Words run together.
        ("moyfiltri", "OIL", "moy filtri"),
        # The wrong keyboard layout, both ways.
        ("cdtxf", "PLUG", "свеча"),
        ("лщдщвлф", "PAD", "kolodka"),
        # Found as typed: no apostrophe, any word order, part-type names, sentences.
        ("yoqilgi filtri", "FUEL", None),
        ("масляный фильтр", "OIL", None),
        ("катушка зажигания", "COIL", None),
        ("Cobalt uchun svecha kerak", "PLUG", None),
        ("нужны колодки для кобальт", "PAD", None),
        # Words the catalog has never seen are left out, and the page says so.
        ("колодки для моей ласточки", "PAD", "колодки"),
    ],
)
def test_misspelled_or_loosely_typed_searches_find_the_part(
    session: Session, typed: str, expected_id: str, corrected: str | None
) -> None:
    response = search_products(session, typed)
    assert response.items, typed
    assert response.items[0].id == expected_id
    assert response.corrected_query == corrected


def test_correct_spellings_and_nonsense_are_left_alone(session: Session) -> None:
    for typed in ("svecha", "moy filtri", "свеча"):
        assert search_products(session, typed).corrected_query is None
    nonsense = search_products(session, "qwerty")
    assert nonsense.total == 0 and nonsense.corrected_query is None


def test_wrong_layout_swaps_only_the_unknown_word(session: Session) -> None:
    vocabulary = load_vocabulary(session)
    assert swap_keyboard_layout("cobalt cdtxf", vocabulary) == "cobalt свеча"
    assert swap_keyboard_layout("cobalt svecha", vocabulary) is None


def test_every_plausible_fix_is_offered_best_first(session: Session) -> None:
    options = correction_options("svica", load_vocabulary(session))
    assert options[0] == "svecha"
    assert len(options) == len(set(options))


@pytest.fixture
def client():
    factory = sessionmaker(make_engine(), expire_on_commit=False)

    def override_session():
        with factory() as session:
            yield session

    previous = settings.pilot_mode
    settings.pilot_mode = True
    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as test_client:
            test_client.factory = factory
            yield test_client
    finally:
        settings.pilot_mode = previous
        app.dependency_overrides.clear()


def test_suggestions_offer_the_fix_part_types_and_parts(client) -> None:
    data = client.get("/api/v1/suggest", params={"q": "svica"}).json()
    assert data["corrected_query"] == "svecha"
    assert data["part_types"][0]["id"] == "CAT-IGN-PLUG"
    assert data["part_types"][0]["part_count"] == 1
    assert data["products"][0]["id"] == "PLUG"

    assert client.get("/api/v1/suggest", params={"q": "s"}).json() == {
        "query": "s",
        "part_types": [],
        "products": [],
    }
    # Keystrokes are not searches.
    with client.factory() as session:
        assert session.scalar(select(func.count(SearchEvent.id))) == 0
