"""Standard part groups and part types for the customer browse filters.

The IRIZON workbook's Categories sheet is the source of truth: its rows are imported first
and always win. This list adds the mechanical part types a car needs that the workbook does
not define yet, so customers can browse the whole car even before every type is stocked. It
also repeats the workbook's own types (brake pads, spark plugs, ...) so a catalog built from
sellers' price lists alone has them; where the workbook was imported its rows are kept.
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
        PartType("CAT-ENG-TCHAIN", "GRM zanjiri (sep) va bashmaklar", "Цепь ГРМ и успокоители",
                 "Timing chain & guides"),
        PartType("CAT-ENG-HEAD", "Silindrlar kallagi (golovka)", "Головка блока цилиндров",
                 "Cylinder head"),
        PartType("CAT-ENG-GSK", "Prokladkalar (kollektor, karter va boshqa)",
                 "Прокладки двигателя (коллектор, поддон и др.)", "Engine gaskets"),
        PartType("CAT-ENG-SEALS", "Salniklar", "Сальники", "Oil seals"),
        PartType("CAT-ENG-CAM", "Taqsimlash vali salnigi", "Сальник распредвала", "Camshaft seal"),
        PartType("CAT-ENG-CRANK", "Tirsakli val salnigi", "Сальник коленвала", "Crankshaft seal"),
        PartType("CAT-ENG-VSEAL", "Klapan salniklari", "Маслосъёмные колпачки (сальник клапана)",
                 "Valve stem seals"),
        PartType("CAT-ENG-VALVE", "Klapanlar va gidrokompensatorlar", "Клапаны и гидрокомпенсаторы",
                 "Valves & lifters"),
        PartType("CAT-ENG-CAMSH", "Taqsimlash vali (raspredval)", "Распредвал", "Camshaft"),
        PartType("CAT-ENG-CRSH", "Tirsakli val (kolenval) va shatunlar", "Коленвал и шатуны",
                 "Crankshaft & connecting rods"),
        PartType("CAT-ENG-BRG", "Vkladishlar", "Вкладыши коленвала", "Crankshaft bearing shells"),
        PartType("CAT-ENG-LINER", "Gilzalar", "Гильзы цилиндров", "Cylinder liners"),
        PartType("CAT-ENG-CAP", "Moy quyish qopqog'i", "Крышка маслозаливной горловины",
                 "Oil filler cap"),
        PartType("CAT-ENG-OTHER", "Dvigatelning boshqa qismlari (karter, shkiv, sapun)",
                 "Прочие детали двигателя (поддон, шкив, сапун)", "Other engine parts"),
    )),
    PartGroup("CAT-FLT", "Filtrlar", "Фильтры", "Filters", (
        PartType("CAT-FLT-AIR", "Havo filtri", "Фильтр воздушный", "Air filter"),
        PartType("CAT-FLT-CAB", "Salon filtri", "Фильтр салона", "Cabin filter"),
        PartType("CAT-FLT-OIL", "Moy filtri", "Фильтр масляный", "Oil filter"),
        PartType("CAT-FLT-FUEL", "Yoqilg'i filtri", "Фильтр топливный", "Fuel filter"),
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
        PartType("CAT-BRK-PAD", "Tormoz kolodkalari", "Колодки тормозные", "Brake pads"),
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
        PartType("CAT-BRK-REG", "Tormoz bosimi regulyatori (legushka)",
                 "Регулятор давления тормозов («лягушка»)", "Brake pressure regulator"),
        PartType("CAT-BRK-VAC", "Vakuum kuchaytirgich va klapani",
                 "Вакуумный усилитель и обратный клапан", "Brake booster & check valve"),
    )),
    PartGroup("CAT-SUS", "Osma", "Подвеска", "Suspension", (
        PartType("CAT-SUS-SHOCK", "Amortizator", "Амортизатор", "Shock absorber"),
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
        PartType("CAT-SUS-KNUCK", "Burilish mushti (kulak)", "Поворотный кулак",
                 "Steering knuckle"),
        PartType("CAT-SUS-LEAF", "Ressor", "Рессора", "Leaf spring"),
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
        PartType("CAT-STR-OTHER", "Rulning boshqa qismlari (kolonka, bachok, shlang)",
                 "Прочие детали рулевого (колонка, бачок, шланг)", "Other steering parts"),
    )),
    PartGroup("CAT-IGN", "O't oldirish tizimi", "Система зажигания", "Ignition system", (
        PartType("CAT-IGN-PLUG", "O't oldirish shamlari (svecha)", "Свечи зажигания",
                 "Spark plugs"),
        PartType("CAT-IGN-COIL", "O't oldirish g'altagi (babina)", "Катушка зажигания (бабина)",
                 "Ignition coil"),
        PartType("CAT-IGN-WIRE", "Svecha simlari to'plami", "Провода высоковольтные",
                 "Ignition lead set"),
        PartType("CAT-IGN-BOOT", "Babina mushtugi (uchligi)",
                 "Наконечник катушки зажигания (муштук)", "Ignition coil boot"),
        PartType("CAT-IGN-MOD", "O't oldirish moduli", "Модуль зажигания", "Ignition module"),
    )),
    PartGroup("CAT-FUEL", "Yoqilg'i tizimi", "Топливная система", "Fuel system", (
        PartType("CAT-FUEL-PUMP", "Benzonasos", "Бензонасос", "Fuel pump"),
        PartType("CAT-FUEL-MOD", "Benzonasos moduli (yig'ilgan)",
                 "Модуль топливного насоса в сборе", "Fuel pump module"),
        PartType("CAT-FUEL-STR", "Benzonasos setkasi (pampers)", "Сетка бензонасоса (памперс)",
                 "Fuel pump strainer"),
        PartType("CAT-FUEL-INJ", "Forsunka (injektor)", "Форсунка (инжектор)", "Fuel injector"),
        PartType("CAT-FUEL-IAC", "Salt yurish datchigi (bochka)", "Регулятор холостого хода",
                 "Idle air control valve"),
        PartType("CAT-FUEL-THR", "Drossel zaslonkasi", "Дроссельная заслонка", "Throttle body"),
        PartType("CAT-FUEL-REG", "Yoqilg'i bosimi regulyatori", "Регулятор давления топлива",
                 "Fuel pressure regulator"),
        PartType("CAT-FUEL-CARB", "Karbyurator", "Карбюратор", "Carburettor"),
        PartType("CAT-FUEL-GAS", "Gaz pedali va trosi", "Педаль и трос газа",
                 "Accelerator pedal & cable"),
    )),
    PartGroup("CAT-COOL", "Sovutish va isitish", "Охлаждение и отопление", "Cooling & heating", (
        PartType("CAT-COOL-THERM", "Termostat", "Термостат", "Thermostat"),
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
        PartType("CAT-COOL-ACP", "Konditsionerning boshqa qismlari", "Детали кондиционера",
                 "A/C parts"),
        PartType("CAT-COOL-HEAT", "Pechka radiatori", "Радиатор отопителя (печка)", "Heater core"),
        PartType("CAT-COOL-HTR", "Pechka qismlari (motor, kran, tros)",
                 "Детали печки (мотор, кран, трос)", "Heater parts"),
    )),
    PartGroup("CAT-EL", "Elektr jihozlari", "Электрооборудование", "Electrical", (
        PartType("CAT-EL-ALT", "Generator", "Генератор", "Alternator"),
        PartType("CAT-EL-BATT", "Akkumulyator", "Аккумулятор", "Battery"),
        PartType("CAT-EL-START", "Starter", "Стартер", "Starter motor"),
        PartType("CAT-EL-SENS", "Datchiklar", "Датчики", "Sensors"),
        PartType("CAT-EL-RELAY", "Saqlagich va rele", "Предохранители и реле", "Fuses & relays"),
        PartType("CAT-EL-SW", "Fara pereklyuchateli (gitara)", "Подрулевой переключатель (гитара)",
                 "Combination switch"),
        PartType("CAT-EL-BULB", "Fara lampasi", "Лампа фары", "Headlight bulb"),
        PartType("CAT-EL-DASH", "Asboblar paneli va spidometr", "Приборная панель и спидометр",
                 "Instrument panel & speedometer"),
        PartType("CAT-EL-WIRE", "Simlar va razyomlar", "Провода и разъёмы", "Wiring & connectors"),
    )),
    PartGroup("CAT-DRV", "Transmissiya va yarim o'qlar", "Трансмиссия и привод", "Driveline", (
        PartType("CAT-DRV-CV", "Yarim o'q sharniri (granata)", "ШРУС (граната)", "CV joint"),
        PartType("CAT-DRV-CLKIT", "Ilashish muftasi to'plami (stsepleniye)",
                 "Комплект сцепления", "Clutch kit"),
        PartType("CAT-DRV-CLBRG", "Ilashish podshipnigi (vyjimnoy)", "Выжимной подшипник",
                 "Clutch release bearing"),
        PartType("CAT-DRV-CLCAB", "Ilashish trosi", "Трос сцепления", "Clutch cable"),
        PartType("CAT-DRV-CLCYL", "Ilashish silindrlari", "Цилиндры сцепления", "Clutch cylinders"),
        PartType("CAT-DRV-BOOT", "Granata pilnigi", "Пыльник ШРУСа", "CV joint boot"),
        PartType("CAT-DRV-SHAFT", "Yarim o'q (privod)", "Привод (полуось) в сборе",
                 "Drive shaft"),
        PartType("CAT-DRV-GBMNT", "Karobka yostig'i (podushka)", "Опора КПП (подушка)",
                 "Gearbox mount"),
        PartType("CAT-DRV-SEAL", "Yarim o'q salnigi", "Сальник полуоси", "Drive shaft seal"),
        PartType("CAT-DRV-GBX", "Uzatmalar qutisi qismlari (sinxron, shesternya)",
                 "Детали КПП (синхронизатор, шестерни)", "Gearbox parts"),
        PartType("CAT-DRV-BRG", "Podshipniklar", "Подшипники", "Bearings"),
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
        PartType("CAT-BODY-LAMP", "Boshqa chiroqlar (povorotnik, plafon)",
                 "Прочие фонари (поворотник, плафон)", "Other lights"),
        PartType("CAT-BODY-WIN", "Oyna ko'targich (steklopodyomnik)", "Стеклоподъёмник",
                 "Window regulator"),
        PartType("CAT-BODY-WMECH", "Oyna tozalagich mexanizmi", "Механизм стеклоочистителя",
                 "Wiper motor & linkage"),
        PartType("CAT-BODY-SEAL", "Rezina zichlagichlar", "Резиновые уплотнители",
                 "Rubber seals"),
        PartType("CAT-BODY-OTHER", "Kuzov detallari (qulf, dastak, tros)",
                 "Детали кузова (замки, ручки, тросы)", "Body parts (locks, handles, cables)"),
    )),
    PartGroup("CAT-CHEM", "Avtokimyo", "Автохимия", "Car care chemicals"),
    PartGroup("CAT-ACC", "Aksessuar va asboblar", "Аксессуары и инструмент",
              "Accessories & tools", (
        PartType("CAT-ACC-FAST", "Bolt, gayka va shpilkalar", "Болты, гайки и шпильки",
                 "Bolts, nuts & studs"),
    )),
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

@dataclass(frozen=True)
class JobPart:
    type_id: str
    # FRONT or REAR when the job needs one end only ("front brakes"); None for either.
    position: str | None = None


@dataclass(frozen=True)
class Job:
    """A common repair and the part types it needs, so a buyer gets the whole list at once."""

    id: str
    name_uz: str
    name_ru: str
    name_en: str
    icon: str
    parts: tuple[JobPart, ...]


JOBS: tuple[Job, ...] = (
    Job("oil-service", "Moy almashtirish", "Замена масла и фильтров", "Oil & filter change",
        "CAT-OIL", (JobPart("CAT-FLT-OIL"), JobPart("CAT-OIL-ENG"), JobPart("CAT-FLT-AIR"),
                    JobPart("CAT-FLT-CAB"))),
    Job("front-brakes", "Oldi tormozlar", "Передние тормоза", "Front brakes", "CAT-BRK",
        (JobPart("CAT-BRK-PAD", "FRONT"), JobPart("CAT-BRK-DISC", "FRONT"),
         JobPart("CAT-BRK-HOSE", "FRONT"), JobPart("CAT-OIL-BRK"))),
    Job("rear-brakes", "Orqa tormozlar", "Задние тормоза", "Rear brakes", "CAT-BRK",
        (JobPart("CAT-BRK-SHOE"), JobPart("CAT-BRK-DRUM"), JobPart("CAT-BRK-WCYL"),
         JobPart("CAT-BRK-PAD", "REAR"), JobPart("CAT-BRK-CABLE"))),
    Job("timing", "GRM almashtirish", "Замена ГРМ", "Timing belt or chain", "CAT-ENG",
        (JobPart("CAT-ENG-TBELT"), JobPart("CAT-ENG-TCHAIN"), JobPart("CAT-ENG-TTEN"),
         JobPart("CAT-COOL-PUMP"), JobPart("CAT-ENG-CAM"), JobPart("CAT-ENG-CRANK"))),
    Job("ignition", "O't oldirish tizimi", "Зажигание", "Ignition service", "CAT-IGN",
        (JobPart("CAT-IGN-PLUG"), JobPart("CAT-IGN-WIRE"), JobPart("CAT-IGN-COIL"),
         JobPart("CAT-IGN-BOOT"))),
    Job("cooling", "Sovutish tizimi", "Система охлаждения", "Cooling system", "CAT-COOL",
        (JobPart("CAT-COOL-THERM"), JobPart("CAT-COOL-PUMP"), JobPart("CAT-COOL-HOSE"),
         JobPart("CAT-COOL-TANK"), JobPart("CAT-COOL-RAD"), JobPart("CAT-OIL-COOL"))),
    Job("clutch", "Ilashish (stsepleniye)", "Сцепление", "Clutch", "CAT-DRV",
        (JobPart("CAT-DRV-CLKIT"), JobPart("CAT-DRV-CLBRG"), JobPart("CAT-DRV-CLCAB"),
         JobPart("CAT-DRV-CLCYL"))),
    Job("front-suspension", "Oldi osma", "Передняя подвеска", "Front suspension", "CAT-SUS",
        (JobPart("CAT-SUS-SHOCK", "FRONT"), JobPart("CAT-SUS-MOUNT", "FRONT"),
         JobPart("CAT-SUS-BALL"), JobPart("CAT-SUS-LINK", "FRONT"), JobPart("CAT-STR-TIE"),
         JobPart("CAT-SUS-HUB", "FRONT"))),
    Job("engine-rebuild", "Dvigatel kapital ta'miri", "Капремонт двигателя", "Engine rebuild",
        "CAT-ENG", (JobPart("CAT-ENG-PIST"), JobPart("CAT-ENG-BRG"), JobPart("CAT-ENG-LINER"),
                    JobPart("CAT-ENG-HGSK"), JobPart("CAT-ENG-GSK"), JobPart("CAT-ENG-VSEAL"),
                    JobPart("CAT-ENG-CRANK"))),
    Job("fuel", "Yoqilg'i tizimi", "Топливная система", "Fuel system", "CAT-FUEL",
        (JobPart("CAT-FUEL-PUMP"), JobPart("CAT-FUEL-STR"), JobPart("CAT-FLT-FUEL"),
         JobPart("CAT-FUEL-INJ"))),
)

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
