"""Standard part groups and part types for the customer browse filters.

The IRIZON workbook's Categories sheet is the source of truth: its rows are imported first
and always win. This list only adds the mechanical part types a car needs that the workbook
does not define yet, so customers can browse the whole car even before every type is stocked.
Types the workbook already defines (brake pads, spark plugs, ...) are not repeated here.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Category, Fitment, Product


@dataclass(frozen=True)
class PartType:
    id: str
    name_uz: str
    name_ru: str
    name_en: str


@dataclass(frozen=True)
class PartGroup(PartType):
    types: tuple[PartType, ...] = ()


# Display order of the browse page: the most commonly needed systems first.
PART_GROUPS: tuple[PartGroup, ...] = (
    PartGroup("CAT-ENG", "Dvigatel", "Двигатель", "Engine", (
        PartType("CAT-ENG-TBELT", "GRM tasmasi (remen)", "Ремень ГРМ", "Timing belt"),
        PartType("CAT-ENG-TTEN", "GRM roligi (natyajitel)", "Ролик натяжителя ГРМ",
                 "Timing belt tensioner"),
        PartType("CAT-ENG-DBELT", "Generator tasmasi (remen)", "Приводной ремень",
                 "Drive belt"),
        PartType("CAT-ENG-HGSK", "Kallak prokladkasi", "Прокладка ГБЦ",
                 "Cylinder head gasket"),
        PartType("CAT-ENG-VCGSK", "Klapan qopqog'i prokladkasi",
                 "Прокладка клапанной крышки", "Valve cover gasket"),
        PartType("CAT-ENG-PIST", "Porshen va porshen halqalari", "Поршни и поршневые кольца",
                 "Pistons & rings"),
        PartType("CAT-ENG-OPUMP", "Moy nasosi", "Масляный насос", "Oil pump"),
        PartType("CAT-ENG-MOUNT", "Dvigatel yostig'i (podushka)", "Опора двигателя (подушка)",
                 "Engine mount"),
    )),
    PartGroup("CAT-FLT", "Filtrlar", "Фильтры", "Filters", (
        PartType("CAT-FLT-AIR", "Havo filtri", "Фильтр воздушный", "Air filter"),
        PartType("CAT-FLT-CAB", "Salon filtri", "Фильтр салона", "Cabin filter"),
    )),
    PartGroup("CAT-OIL", "Moylar va suyuqliklar", "Масла и технические жидкости",
              "Oils & fluids", (
        PartType("CAT-OIL-ENG", "Motor moyi", "Моторное масло", "Engine oil"),
        PartType("CAT-OIL-GEAR", "Uzatmalar qutisi moyi", "Трансмиссионное масло", "Gear oil"),
        PartType("CAT-OIL-COOL", "Antifriz (sovutish suyuqligi)",
                 "Антифриз (охлаждающая жидкость)", "Antifreeze / coolant"),
        PartType("CAT-OIL-BRK", "Tormoz suyuqligi", "Тормозная жидкость", "Brake fluid"),
        PartType("CAT-OIL-PS", "Gidrokuchaytirgich (GUR) moyi", "Жидкость ГУР",
                 "Power steering fluid"),
        PartType("CAT-OIL-WASH", "Oyna yuvish suyuqligi", "Жидкость стеклоомывателя",
                 "Washer fluid"),
    )),
    PartGroup("CAT-BRK", "Tormoz tizimi", "Тормозная система", "Braking", (
        PartType("CAT-BRK-DISC", "Tormoz disklari", "Диски тормозные", "Brake discs"),
        PartType("CAT-BRK-SHOE", "Baraban kolodkalari", "Колодки барабанные", "Brake shoes"),
        PartType("CAT-BRK-DRUM", "Tormoz barabani", "Барабан тормозной", "Brake drum"),
        PartType("CAT-BRK-CAL", "Tormoz supporti", "Суппорт тормозной", "Brake caliper"),
        PartType("CAT-BRK-MCYL", "Tormoz bosh silindri", "Главный тормозной цилиндр",
                 "Brake master cylinder"),
        PartType("CAT-BRK-WCYL", "G'ildirak tormoz silindri", "Рабочий тормозной цилиндр",
                 "Wheel brake cylinder"),
        PartType("CAT-BRK-HOSE", "Tormoz shlangi", "Шланг тормозной", "Brake hose"),
        PartType("CAT-BRK-CABLE", "Qo'l tormozi trosi", "Трос стояночного тормоза",
                 "Handbrake cable"),
        PartType("CAT-BRK-ABS", "ABS datchigi", "Датчик ABS", "ABS sensor"),
    )),
    PartGroup("CAT-SUS", "Osma", "Подвеска", "Suspension", (
        PartType("CAT-SUS-SPRING", "Prujina", "Пружина подвески", "Coil spring"),
        PartType("CAT-SUS-MOUNT", "Amortizator tayanchi (opora)", "Опора амортизатора",
                 "Strut mount"),
        PartType("CAT-SUS-ARM", "Richag", "Рычаг подвески", "Control arm"),
        PartType("CAT-SUS-BALL", "Shar tayanchi (sharovoy)", "Шаровая опора", "Ball joint"),
        PartType("CAT-SUS-LINK", "Stabilizator stoykasi", "Стойка стабилизатора",
                 "Stabilizer link"),
        PartType("CAT-SUS-BUSH", "Saylentblok va vtulkalar", "Сайлентблоки и втулки",
                 "Bushings"),
        PartType("CAT-SUS-HUB", "G'ildirak podshipnigi (stupitsa)", "Подшипник ступицы",
                 "Wheel bearing"),
    )),
    PartGroup("CAT-STR", "Rul boshqaruvi", "Рулевое управление", "Steering", (
        PartType("CAT-STR-TIE", "Rul uchligi (nakonechnik)", "Рулевой наконечник",
                 "Tie rod end"),
        PartType("CAT-STR-ROD", "Rul tyagasi", "Рулевая тяга", "Tie rod"),
        PartType("CAT-STR-RACK", "Rul reykasi", "Рулевая рейка", "Steering rack"),
        PartType("CAT-STR-BOOT", "Rul reykasi pilnigi", "Пыльник рулевой рейки",
                 "Steering rack boot"),
        PartType("CAT-STR-PUMP", "Gidrokuchaytirgich nasosi (GUR)", "Насос ГУР",
                 "Power steering pump"),
    )),
    PartGroup("CAT-IGN", "O't oldirish tizimi", "Система зажигания", "Ignition system"),
    PartGroup("CAT-FUEL", "Yoqilg'i tizimi", "Топливная система", "Fuel system", (
        PartType("CAT-FUEL-THR", "Drossel zaslonkasi", "Дроссельная заслонка", "Throttle body"),
        PartType("CAT-FUEL-REG", "Yoqilg'i bosimi regulyatori", "Регулятор давления топлива",
                 "Fuel pressure regulator"),
    )),
    PartGroup("CAT-COOL", "Sovutish va isitish", "Охлаждение и отопление", "Cooling & heating", (
        PartType("CAT-COOL-RAD", "Sovutish radiatori", "Радиатор охлаждения", "Radiator"),
        PartType("CAT-COOL-PUMP", "Suv nasosi (pompa)", "Помпа (водяной насос)", "Water pump"),
        PartType("CAT-COOL-FAN", "Radiator ventilyatori", "Вентилятор радиатора",
                 "Radiator fan"),
        PartType("CAT-COOL-HOSE", "Radiator shlangi (patrubka)", "Патрубок радиатора",
                 "Radiator hose"),
        PartType("CAT-COOL-TANK", "Kengaytirish bachogi", "Расширительный бачок",
                 "Expansion tank"),
        PartType("CAT-COOL-AC", "Konditsioner kompressori", "Компрессор кондиционера",
                 "A/C compressor"),
    )),
    PartGroup("CAT-EL", "Elektr jihozlari", "Электрооборудование", "Electrical", (
        PartType("CAT-EL-START", "Starter", "Стартер", "Starter motor"),
        PartType("CAT-EL-SENS", "Datchiklar", "Датчики", "Sensors"),
        PartType("CAT-EL-RELAY", "Saqlagich va rele", "Предохранители и реле", "Fuses & relays"),
    )),
    PartGroup("CAT-DRV", "Transmissiya va yarim o'qlar", "Трансмиссия и привод", "Driveline", (
        PartType("CAT-DRV-CLKIT", "Ilashish muftasi to'plami (stsepleniye)",
                 "Комплект сцепления", "Clutch kit"),
        PartType("CAT-DRV-CLBRG", "Ilashish podshipnigi (vyjimnoy)", "Выжимной подшипник",
                 "Clutch release bearing"),
        PartType("CAT-DRV-CLCAB", "Ilashish trosi", "Трос сцепления", "Clutch cable"),
        PartType("CAT-DRV-BOOT", "Granata pilnigi", "Пыльник ШРУСа", "CV joint boot"),
        PartType("CAT-DRV-SHAFT", "Yarim o'q (privod)", "Привод (полуось) в сборе",
                 "Drive shaft"),
        PartType("CAT-DRV-GBMNT", "Karobka yostig'i (podushka)", "Опора КПП (подушка)",
                 "Gearbox mount"),
    )),
    PartGroup("CAT-EXH", "Chiqarish tizimi (glushitel)", "Выхлопная система", "Exhaust", (
        PartType("CAT-EXH-MUF", "Glushitel", "Глушитель", "Muffler"),
        PartType("CAT-EXH-PIPE", "Rezonator va quvurlar", "Резонатор и трубы",
                 "Resonator & pipes"),
        PartType("CAT-EXH-CAT", "Katalizator", "Катализатор", "Catalytic converter"),
        PartType("CAT-EXH-O2", "Lyambda zond (kislorod datchigi)", "Лямбда-зонд",
                 "Oxygen sensor"),
        PartType("CAT-EXH-GSK", "Glushitel prokladkasi va xomutlari",
                 "Прокладки и хомуты глушителя", "Exhaust gaskets & clamps"),
    )),
    PartGroup("CAT-BODY", "Kuzov va chiroqlar", "Кузов и освещение", "Body & lights", (
        PartType("CAT-BODY-WIPER", "Oyna tozalagich (dvornik)", "Щётки стеклоочистителя",
                 "Wiper blades"),
        PartType("CAT-BODY-HEAD", "Fara", "Фара", "Headlight"),
        PartType("CAT-BODY-TAIL", "Orqa chiroq (stop)", "Задний фонарь", "Tail light"),
        PartType("CAT-BODY-MIRROR", "Yon oyna (ko'zgu)", "Боковое зеркало", "Side mirror"),
    )),
    PartGroup("CAT-CHEM", "Avtokimyo", "Автохимия", "Car care chemicals"),
    PartGroup("CAT-ACC", "Aksessuar va asboblar", "Аксессуары и инструмент",
              "Accessories & tools"),
)

# Parts usually replaced in the same job ("Complete the job"), by part type.
COMPLETE_THE_JOB: dict[str, tuple[str, ...]] = {
    "CAT-IGN-PLUG": ("CAT-IGN-WIRE", "CAT-IGN-BOOT", "CAT-IGN-COIL"),
    "CAT-IGN-COIL": ("CAT-IGN-BOOT", "CAT-IGN-PLUG"),
    "CAT-IGN-BOOT": ("CAT-IGN-COIL", "CAT-IGN-PLUG"),
    "CAT-IGN-WIRE": ("CAT-IGN-PLUG",),
    "CAT-IGN-MOD": ("CAT-IGN-COIL", "CAT-IGN-PLUG"),
    "CAT-BRK-PAD": ("CAT-BRK-DISC", "CAT-OIL-BRK", "CAT-CHEM-BRK"),
    "CAT-BRK-DISC": ("CAT-BRK-PAD", "CAT-CHEM-BRK"),
    "CAT-BRK-SHOE": ("CAT-BRK-DRUM", "CAT-BRK-WCYL"),
    "CAT-FLT-OIL": ("CAT-OIL-ENG", "CAT-FLT-AIR", "CAT-FLT-CAB"),
    "CAT-OIL-ENG": ("CAT-FLT-OIL",),
    "CAT-FLT-AIR": ("CAT-FLT-OIL", "CAT-FLT-CAB"),
    "CAT-FLT-FUEL": ("CAT-FUEL-STR", "CAT-FUEL-PUMP"),
    "CAT-FUEL-PUMP": ("CAT-FUEL-STR", "CAT-FLT-FUEL", "CAT-FUEL-CON"),
    "CAT-FUEL-MOD": ("CAT-FUEL-STR", "CAT-FLT-FUEL"),
    "CAT-FUEL-STR": ("CAT-FUEL-PUMP", "CAT-FLT-FUEL"),
    "CAT-FUEL-INJ": ("CAT-FLT-FUEL", "CAT-CHEM-FUEL"),
    "CAT-FUEL-IAC": ("CAT-CHEM-CARB", "CAT-FUEL-THR"),
    "CAT-COOL-THERM": ("CAT-OIL-COOL", "CAT-COOL-HOSE"),
    "CAT-COOL-HEAT": ("CAT-OIL-COOL",),
    "CAT-COOL-RAD": ("CAT-OIL-COOL", "CAT-COOL-HOSE", "CAT-COOL-THERM"),
    "CAT-COOL-PUMP": ("CAT-ENG-TBELT", "CAT-OIL-COOL", "CAT-COOL-THERM"),
    "CAT-ENG-TBELT": ("CAT-ENG-TTEN", "CAT-COOL-PUMP", "CAT-ENG-CAM", "CAT-ENG-CRANK"),
    "CAT-ENG-HEAD": ("CAT-ENG-HGSK", "CAT-ENG-VSEAL", "CAT-ENG-CAM"),
    "CAT-ENG-VSEAL": ("CAT-ENG-VCGSK", "CAT-ENG-CAM"),
    "CAT-ENG-CAM": ("CAT-ENG-CRANK", "CAT-ENG-TBELT"),
    "CAT-ENG-CRANK": ("CAT-ENG-CAM", "CAT-ENG-TBELT"),
    "CAT-DRV-CV": ("CAT-DRV-BOOT", "CAT-DRV-SEAL", "CAT-OIL-GEAR"),
    "CAT-DRV-SEAL": ("CAT-DRV-CV", "CAT-OIL-GEAR"),
    "CAT-SUS-SHOCK": ("CAT-SUS-MOUNT", "CAT-SUS-SPRING"),
    "CAT-EL-BATT": ("CAT-EL-ALT",),
    "CAT-EL-ALT": ("CAT-EL-BATT", "CAT-ENG-DBELT"),
    "CAT-EL-BULB": ("CAT-BODY-HEAD",),
}

_ORDER = {
    category.id: index
    for index, category in enumerate(
        category for group in PART_GROUPS for category in (group, *group.types)
    )
}


def ensure_standard_part_types(session: Session) -> int:
    """Add the standard groups and types the catalog lacks; never touches existing rows."""
    existing = set(session.scalars(select(Category.id)))
    added = [
        Category(
            id=category.id,
            parent_id=None if category is group else group.id,
            name_uz=category.name_uz,
            name_ru=category.name_ru,
            name_en=category.name_en,
            is_leaf=category is not group,
        )
        for group in PART_GROUPS
        for category in (group, *group.types)
        if category.id not in existing
    ]
    # Groups go first so a new type's parent exists before it.
    for category in added:
        session.add(category)
        session.flush()
    return len(added)


def _paths(categories: dict[str, Category]) -> dict[str, list[str]]:
    """Map every category to its ancestry, from itself up to its top-level group."""
    paths: dict[str, list[str]] = {}
    for category in categories.values():
        path = [category.id]
        node = category
        while node.parent_id in categories and node.parent_id not in path:
            node = categories[node.parent_id]
            path.append(node.id)
        paths[category.id] = path
    return paths


def category_with_descendants(session: Session, category_id: str) -> set[str]:
    """The category and everything below it; empty when the category does not exist."""
    categories = {category.id: category for category in session.scalars(select(Category))}
    return {candidate for candidate, path in _paths(categories).items() if category_id in path}


def fits_vehicles(vehicle_ids: set[str]):
    """Parts fitted to one of these vehicles, or universal parts that fit every car."""
    return or_(
        Product.universal.is_(True),
        Product.fitments.any(Fitment.vehicle_id.in_(vehicle_ids)),
    )


def part_groups(session: Session, vehicle_ids: set[str] | None = None) -> list[dict]:
    """Every part group with its part types and searchable part counts."""
    categories = {category.id: category for category in session.scalars(select(Category))}
    stmt = (
        select(Product.category_id, func.count(Product.id))
        .where(Product.is_searchable.is_(True), Product.category_id.is_not(None))
        .group_by(Product.category_id)
    )
    if vehicle_ids is not None:
        stmt = stmt.where(fits_vehicles(vehicle_ids))
    counts: dict[str, int] = dict(session.execute(stmt).all())

    groups: dict[str, dict] = {}
    types: dict[str, dict] = {}

    def entry(category: Category) -> dict:
        return {
            "id": category.id,
            "name_uz": category.name_uz,
            "name_ru": category.name_ru,
            "name_en": category.name_en,
            "part_count": 0,
        }

    # Deeper levels roll up into the part type directly below their group.
    for category_id, path in _paths(categories).items():
        group_id, type_id = path[-1], path[-2] if len(path) > 1 else path[-1]
        group = groups.setdefault(group_id, {**entry(categories[group_id]), "types": []})
        if type_id != group_id and type_id not in types:
            types[type_id] = entry(categories[type_id])
            group["types"].append(types[type_id])
        count = counts.get(category_id, 0)
        group["part_count"] += count
        if type_id != group_id:
            types[type_id]["part_count"] += count

    def order(item: dict) -> tuple[int, str]:
        return _ORDER.get(item["id"], len(_ORDER)), item["id"]

    for group in groups.values():
        group["types"].sort(key=order)
    return sorted(groups.values(), key=order)
