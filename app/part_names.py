"""Read the part names sellers write in their price lists.

Sellers name parts in shorthand and slang, in Latin or Cyrillic, with the part number and
position mixed in: "KALODKA OLDI (96273708) PREMIUM", "ABC DACHCHIK OLDI LH 94544449",
"амортизатор передней". This module turns such a name into a part type, the position,
side and size it describes, its part numbers, and a clean name in Uzbek, Russian and English.
The seller's own wording is kept elsewhere so searches in the same slang still find the part.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Cyrillic to the Latin letters sellers use for the same sounds ("XITOY", "SUXARIK").
_LATIN = str.maketrans({
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "YO", "Ж": "J", "З": "Z",
    "И": "I", "Й": "Y", "К": "K", "Л": "L", "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R",
    "С": "S", "Т": "T", "У": "U", "Ф": "F", "Х": "X", "Ц": "TS", "Ч": "CH", "Ш": "SH",
    "Щ": "SH", "Ъ": "", "Ы": "I", "Ь": "", "Э": "E", "Ю": "YU", "Я": "YA", "Ў": "O", "Қ": "Q",
    "Ғ": "G", "Ҳ": "H", "（": "(", "）": ")",
})
# Back to Cyrillic, for Russian names of parts the rules do not recognize ("KULACHOK").
_CYRILLIC = [
    ("SHCH", "Щ"), ("YO", "Ё"), ("YU", "Ю"), ("YA", "Я"), ("CH", "Ч"), ("SH", "Ш"), ("TS", "Ц"),
    ("ZH", "Ж"), ("KH", "Х"), ("A", "А"), ("B", "Б"), ("V", "В"), ("G", "Г"), ("D", "Д"),
    ("E", "Е"), ("J", "Ж"), ("Z", "З"), ("I", "И"), ("Y", "Й"), ("K", "К"), ("L", "Л"),
    ("M", "М"), ("N", "Н"), ("O", "О"), ("P", "П"), ("R", "Р"), ("S", "С"), ("T", "Т"),
    ("U", "У"), ("F", "Ф"), ("X", "Х"), ("H", "Х"), ("Q", "К"), ("W", "В"), ("C", "К"),
]
_NOT_TEXT = re.compile(r"[^\w\s()/.,+&'-]")


def latin_upper(text: str) -> str:
    """Upper-case Latin form of a seller's text, Cyrillic transliterated, Chinese dropped."""
    value = (text or "").upper().translate(_LATIN)
    value = re.sub(r"[　-鿿]+", " ", value)
    return " ".join(_NOT_TEXT.sub(" ", value).split())


def cyrillic(text: str) -> str:
    value = text.upper()
    for latin, letter in _CYRILLIC:
        value = value.replace(latin, letter)
    return value


# Part type rules, most specific first. A rule is a regular expression over latin_upper().
TYPE_RULES: tuple[tuple[str, str], ...] = (
    # A bolt, nut or handle is named first and the part it belongs to after it.
    (r"^(BOLT|GAYKA|SHPILKA|SHAYBA)\b", "CAT-ACC-FAST"),
    (r"RUCHK", "CAT-BODY-OTHER"),
    # Hoses are named by the system they carry fluid for ("TRUPKA SUV ANTFRIZ").
    (r"P[AO]T+R?UBK\w* VO[XZ]DU|GOFRA\w* VO[XZ]DU|BACHOK VO[XZ]DU", "CAT-FLT"),
    (r"^(SHLAN\w*|TRU?PK\w*|TRUBK\w*) .*(ANT[I]?FRIZ|SUV|ZASLONK|SAFUN|SAPUN)", "CAT-COOL-HOSE"),
    (r"BACHO[KG]\w* (DVORNIK|OMIV)|DVORNIK\w* (STOYKA|RICHAG)", "CAT-BODY-WMECH"),
    # Sensors are named after what they measure ("MASLO DACHCHIK", "DACHCHIK RASPREDVAL").
    (r"LYAMBDA|KISLOROD", "CAT-EXH-O2"),
    (r"ABC|\bABS\b", "CAT-BRK-ABS"),
    (r"DA\w{0,3}CHIK", "CAT-EL-SENS"),
    # So are relays ("RELE BENZANASOS" is the fuel pump's relay, not the pump).
    (r"\bRELE\b", "CAT-EL-RELAY"),
    # Gaskets and seals name the part they seal, so they come before that part.
    (r"PROKLAD.*(G[AO]L[AO]VK|GBTS|GBC|BLOK\b)|G[AO]L[AO]VK\w* PROKLAD", "CAT-ENG-HGSK"),
    (r"PROKLAD.*(KRI?SHK|KLAP[AI]N)|KRI?SHK\w* PROKLAD", "CAT-ENG-VCGSK"),
    (r"PROKLAD.*(G[UL]+SH[IE]T|KOL+EKTOR|KAL+EKTOR|VIPUSK|VYPUSK|PRIYOMN|PRIEMN)", "CAT-EXH-GSK"),
    (r"REZINA\w* G[UL]+SH|G[UL]+SH\w* REZINA", "CAT-EXH-GSK"),
    (r"PROKLAD|NABOR|NABORCHA", "CAT-ENG-GSK"),
    (r"MASLOS.?OM|MASLOS.?YOM|KOLPACH", "CAT-ENG-VSEAL"),
    (r"SALNI.*(K[AO]L[EI]N|KOLENCH|TIRSAK)|K[AO]L[EI]NVAL\w* SALNI", "CAT-ENG-CRANK"),
    (r"SALNI.*RAS?P|RAS?P\w*VAL\w* SALNI", "CAT-ENG-CAM"),
    (r"SALNI.*(PRIVOD|GRANAT|POLU?OS|KAR[AO]P?BK|KOROBK|KPP|PEREVECH|VTORICH)", "CAT-DRV-SEAL"),
    (r"SALNI.*KLAP", "CAT-ENG-VSEAL"),
    (r"SALNI|^KOS[ -]?\d", "CAT-ENG-SEALS"),
    # Boots and bump stops belong to the part they protect.
    (r"PIL+N\w*.*(GRANAT|SHRUS)|(GRANAT|SHRUS)\w* PIL+N", "CAT-DRV-BOOT"),
    (r"PIL+N\w*.*(RUL|REYK)|RUL\w* PIL+N", "CAT-STR-BOOT"),
    ((r"PIL+N\w*.*AMORT|AMORT\w* PIL+N|OTBOYNIK|ADBOYNIK|LOLA AMORT|CHASHKA|OPORA|[AO]PORNIK|"
     r"PODUSHK.*(AMORT|STOYK)"), "CAT-SUS-MOUNT"),
    # Bushings, before the arms and links they sit in.
    ((r"[FV]TULKA|SAYLENT|SA[IY]?LENBLOK|SELANBLOK|SELENBLOK|SAYLEN|"
      r"(PODUSHK|REZINA)\w* RES+OR|REZINA (STIL|STAB|STAL)"), "CAT-SUS-BUSH"),
    # Gearbox internals.
    ((r"SINXRON|SINHRON|MUFT[OI]CHKA|PEREVECH|PEREVISH|PERVICH|VTORICH|KUL[IY][SC]A|"
     r"BLOK SHESTERNA|SHESTERNA.*(KPP|M/T|\d M)|FILTER KAR[AO]PK|FILTER KOROBK|"
     r"VILKA (KPP|KAR[AO]P?K|PEREKL)|SKOROST QUYON"), "CAT-DRV-GBX"),
    (r"PODUSHK\w*.*(KAR[AO][PB]K|KOROBK|KPP|STRELKA)|BEZ STRELKA", "CAT-DRV-GBMNT"),
    # Clutch.
    (r"V[IY]?J[IE]?[MN]N?OY|VJEMNOY|VIJIMNOY|VYJIMNOY", "CAT-DRV-CLBRG"),
    ((r"(GL[AO]VN|GILAVNI|RABOCH).*(S[CE]?PLEN|SEPLE|STSEPL)|(S[CE]?PLEN|SEPLE)\w* .*"
     r"(GL[AO]VN|GILAVNI|RABOCH|TSILIND|SILIND)"), "CAT-DRV-CLCYL"),
    (r"TROS.*(S[CE]?PLEN|SEPLE)|(S[CE]?PLEN|SEPLE)\w* TROS", "CAT-DRV-CLCAB"),
    (r"K[AO]RZIN|DISK.*(S[CE]?PLEN|SEPLE)|(S[CE]?PLEN|SEPLE)\w* (DISK|KOMPLEKT)|SEPLENA ZBOR",
     "CAT-DRV-CLKIT"),
    # Drive shafts and CV joints.
    (r"PRIVOD|POLU?OS|POLOS GRANAT|POLOVOS|GRANAT\w* ZB[OA]R|SHLITSA|KARDAN|KR[IE]STOV|KIRISTAV",
     "CAT-DRV-SHAFT"),
    (r"GRANAT|SHRUS|SHARNIR.*(PRIVOD|GRANAT)", "CAT-DRV-CV"),
    # Brakes.
    (r"LEGUSHKA TORMOZ|REGULYATOR.*TORMOZ|KOLDUN", "CAT-BRK-REG"),
    (r"ABRATN|OBRATN|VAKUUM|VAKUM|USILITEL TORMOZ", "CAT-BRK-VAC"),
    (r"(GL[AO]VN|GILAVNI)\w* .*TORMOZ|TORMOZ\w* .*(GL[AO]VN|TSILIND)|GL[AO]VN\w* TSILIND",
     "CAT-BRK-MCYL"),
    (r"RABOCH\w* .*LI?ND|TSI?LIND\w* .*RABOCH", "CAT-BRK-WCYL"),
    (r"TROS.*(RUCHN|ROCHN|STOYANOCH|TORMOZ)|RUCHNOY TROS", "CAT-BRK-CABLE"),
    (r"(SHLAN|TRU?PK|TRUBK).*TORMOZ|TORMOZ\w* (SHLAN|TRU?PK|TRUBK)", "CAT-BRK-HOSE"),
    (r"SUPPORT|SUPORT|PAL[EI][TS]S? .*TORMOZ", "CAT-BRK-CAL"),
    (r"BARABAN\w*.*(OLDI|PEREDN|PERF)|DISK\w* TORMOZ|TORMOZ\w* DISK", "CAT-BRK-DISC"),
    (r"K[AO]L[AO]DK.*(BARABAN|ORQA|ZADN)|BASHMAK TORMOZ", "CAT-BRK-SHOE"),
    (r"K[AO]L[AO]DK|KALOTKA|KOLODK", "CAT-BRK-PAD"),
    (r"BARABAN", "CAT-BRK-DRUM"),
    # Suspension.
    (r"AMORT\w* (BAGAJ|KAPOT)|(BAGAJ|KAPOT)\w* AMORT", "CAT-BODY-OTHER"),
    (r"AMORT|AMARTI|AMORTNZ|STOYKA AMORT|LOLA", "CAT-SUS-SHOCK"),
    (r"RES+OR", "CAT-SUS-LEAF"),
    (r"PR[UO]J[IY]N|PURJINA", "CAT-SUS-SPRING"),
    (r"SHAR[AO]VOY|SHAROV|SHARAV", "CAT-SUS-BALL"),
    (r"ST[AI]L?[IAB]+L?[IB]?Z[AI]?TOR|STABIL|STALBIZ|STILBIZ|STALIB", "CAT-SUS-LINK"),
    (r"STUPI[TDC]+S?A|STUPITS|STUPICH", "CAT-SUS-HUB"),
    ((r"(PODSHI[PB]N|PACHIMNIK)\w*.*(OLDI|ORQA|PEREDN|ZADN|KOLES|G'ILDIRAK)|"
     r"(OLDI|ORQA) PACHIMNIK|\bDT\d{4,}"), "CAT-SUS-HUB"),
    (r"KULAK|KULICHOK POVOROT", "CAT-SUS-KNUCK"),
    (r"RI[CS]HAG|RICHAK|RICHAG|RYCHAG|TRAVERS|BALKA", "CAT-SUS-ARM"),
    # Steering.
    (r"NAK[AO]N[EI]CHN|NAKANESHN|NAKONESHN", "CAT-STR-TIE"),
    (r"SHARN[EI]R|TYAGA|TIYAGA", "CAT-STR-ROD"),
    (r"(RULEV|RULAV|RUL)\w* (REYK|REKA|REYKA|MEXANIZM|MEHANIZM)|REYKA RUL", "CAT-STR-RACK"),
    (r"(GIDRAV|GUR|GIDROUSIL)\w* NASOS|NASOS\w* (GUR|GIDRAV|RUL)", "CAT-STR-PUMP"),
    (r"GIDRAV|GUR\b|RULEV|RULAV|\bRUL\b|MAYATNIK|KALONKA|KOLONKA", "CAT-STR-OTHER"),
    # Ignition.
    (r"SVECH\w* (PRAV|PROV|SIM)|PRAV[AO]DA|PROVOD.*SVECH", "CAT-IGN-WIRE"),
    (r"MUSHTUK|MUNDSHTUK", "CAT-IGN-BOOT"),
    (r"MODUL ZAJIG|MITSUBISI|MODUL.*ZAJIG|TRAMBL|RASPREDELITEL ZAJIG|BEGUNOK", "CAT-IGN-MOD"),
    (r"SVECH", "CAT-IGN-PLUG"),
    (r"BABIN|KATUSHK", "CAT-IGN-COIL"),
    # Filters.
    (r"FIL+T[EI]?R\w* .*(VO[XK]?DU|VOZDU|VOXDUX|HAVO|HAVA)|VOZDUSHN\w* FIL", "CAT-FLT-AIR"),
    (r"FIL+T[EI]?R\w* .*(KONDI|SALON|KABIN)", "CAT-FLT-CAB"),
    (r"FIL+T[EI]?R\w* .*(BEN?Z|BEZIN|TOPLIV|YOQILG|ATISTON|OTSTOY)|TOPLIVN\w* FIL", "CAT-FLT-FUEL"),
    (r"VO[XZ]DU\w* FIL", "CAT-FLT-AIR"),
    (r"FIL+T[EI]?R\w* .*(MAS?LO|MASL|MOY)|MASLYAN\w* FIL", "CAT-FLT-OIL"),
    # Fuel system.
    (r"PAMPERS|SETKA.*BENZ|BENZ\w* SETKA", "CAT-FUEL-STR"),
    (r"BENZ\w*.*(DACH|DATCH)|(DACH|DATCH)\w* BENZ", "CAT-EL-SENS"),
    ((r"BENZ\w* ?NASOS\w* .*(ZBOR|SBOR|MODUL|KRISHK)|BENZ\w*NASOS\w* .*(ZBOR|SBOR|MODUL|KRISHK)|"
     r"BENZ[AO]NASOS KRISHK|BENZANASOS KRISHKA"), "CAT-FUEL-MOD"),
    (r"NASOS\w* TOPLIV\w* .*SBOR", "CAT-FUEL-MOD"),
    (r"BENZ\w* ?NASOS|BENZ[AO]N?A?SOS|TOPLIVN\w* NASOS|NASOS TOPLIV", "CAT-FUEL-PUMP"),
    (r"FORSUN|INJEKTOR|INJEKTR|INJECTOR", "CAT-FUEL-INJ"),
    (r"DROS+EL|ZASLONK", "CAT-FUEL-THR"),
    (r"BOCHKA|XOLOSTOG|XOLOSTOY", "CAT-FUEL-IAC"),
    (r"KARB[IYU]+RATOR|KARBURATOR", "CAT-FUEL-CARB"),
    (r"TROS\w* GAZ|GAZ\w* TROS|PEDAL\w* GAZ|AKSELERATOR|TROS PADSOS", "CAT-FUEL-GAS"),
    # Cooling and heating.
    (r"RADIATOR\w* .*(PECH|OTOPIT)|(PECH|OTOPIT)\w* RADIATOR", "CAT-COOL-HEAT"),
    (r"K[OA]NDI[TC]?S?I?O?N\w* .*KOMPRES|KOMPRES\w* .*KONDI", "CAT-COOL-AC"),
    (r"K[OA]NDI[TC]?S?[IY]?O?N|KONDITSONER|KONDICIONER", "CAT-COOL-ACP"),
    (r"PECH|OTOPIT", "CAT-COOL-HTR"),
    (r"P[AO]T+R?UBK|PATRUBOK|POTRUBK|PODRUBK|TERMAST\w* TRU|SHLANK.*RADIATOR|RADIATOR\w* SHLAN",
     "CAT-COOL-HOSE"),
    (r"TERM[AEO]S?I?TA?TS?|TERMOSTAT|TERMESTAT|TERMASTAT", "CAT-COOL-THERM"),
    (r"POMPA|POMBA|VODYAN\w* NASOS|NASOS\w* VODYAN|SUV NASOS", "CAT-COOL-PUMP"),
    (r"V[EI]NT[EI]L?YATOR|VINTERYATOR|DEFIZOR|DIFFUZOR|LOPIS|LOPAST|KRILCHATKA", "CAT-COOL-FAN"),
    (r"BACHO[KG].*(SUV|RASSHIR|RABOCH|ANTIF|OXLAJ)|RABOCHI\w* BACHO|KRISHKA SUV|SUV KRISHK",
     "CAT-COOL-TANK"),
    (r"RASPREDELITEL VODYAN", "CAT-COOL-HOSE"),
    (r"BACHO[KG].*(GIDRAV|GUR)", "CAT-STR-OTHER"),
    (r"RADIATOR|RADIAROT", "CAT-COOL-RAD"),
    # Engine.
    (r"KOJUX|ZUBCHAT\w* KRISHK|MATOR KRISHK|MOTOR KRISHK|KOL+EKTOR", "CAT-ENG-OTHER"),
    (r"NAT[AY]?[JZ]?[AIE]?[JZ]?I?T[EI]L|NATIJITIL|NATAJITEL|ROLIK|ROLAVOY ROL", "CAT-ENG-TTEN"),
    (r"\bSEP\b|TSEP|ZANJIR|BASHMAK", "CAT-ENG-TCHAIN"),
    (r"REMEN\w* .*(GRM|ZUBCH)|ZUBCHAT\w* REMEN|REMEN GRM", "CAT-ENG-TBELT"),
    (r"REMEN|\d+PK\d+", "CAT-ENG-DBELT"),
    (r"PODUSHK|BINOKL|OPORA DVIG|KRANSHTEYN", "CAT-ENG-MOUNT"),
    (r"MAS?L\w* NASOS|MASLYAN\w* NASOS|MOY NASOS", "CAT-ENG-OPUMP"),
    (r"AFTOL KRISHK|(MAY|MOY|MASLO)\w* KRISHK|KRISHK\w* (MASL|MOY)", "CAT-ENG-CAP"),
    (r"V[KF]LAD[IY]?SH|VKLADSH", "CAT-ENG-BRG"),
    (r"GIL+ZA", "CAT-ENG-LINER"),
    (r"PORSH|\bPOL KOLSA|K[AO]L[TS]?S[AO]|COLSA|CALSO|POLY C?K?ALSO|PALES PORSH", "CAT-ENG-PIST"),
    (r"KLAP[AI]N|GIDROTALKAT|GI?DROKOM|SUXARIK|NAPRAVLYASH|KOROMISLO KLAP|RAKER", "CAT-ENG-VALVE"),
    (r"RAS?P[IE]?R?[IE]?D?VAL|RASPREDVAL|RASPEDVAL|RASPIREDVAL", "CAT-ENG-CAMSH"),
    (r"K[AO]L[EI]N\w*VAL|KOLENCHAT|SHATUN|KALIN VAL", "CAT-ENG-CRSH"),
    (r"G[AO]L[AO]VK\w*|GBTS", "CAT-ENG-HEAD"),
    (r"KARTER|SAPUN|SAFUN|SHKIF|ZAGLUSHK|SHUP|MAXOVIK|VENIS|VENETS|ZVOZDOCHK|SHESTERNA",
     "CAT-ENG-OTHER"),
    # Electrical. Relays before the alternator: "RELE DINAM" is the alternator's relay.
    (r"RELE\b|RELE |PREDOXRAN|PRIDOXNA|PREDOHRAN", "CAT-EL-RELAY"),
    (r"STARTER|BEN?DEKS|BINDEKS|BENDIKS|PUSKACH|PLANTARKA", "CAT-EL-START"),
    (r"DINAM|GENERATOR|STATOR|DIOD", "CAT-EL-ALT"),
    (r"AKKUMULYATOR|\bAKB\b", "CAT-EL-BATT"),
    (r"VKLY?UCHAT|VKLUCHAT|PEREKLYUCH|VIKLYUCH|VYKLYUCH|GITARA|KNOPK", "CAT-EL-SW"),
    (r"LAMP[AO]|LAMPOCHK", "CAT-EL-BULB"),
    (r"SPIDOMET|SKOROS|SKOROST|STRELKA|PRIBOR", "CAT-EL-DASH"),
    (r"GNEZD|RAZYOM|ANTENNA|PROVOD", "CAT-EL-WIRE"),
    # Exhaust.
    (r"KATALIZAT", "CAT-EXH-CAT"),
    (r"GOFR", "CAT-EXH-PIPE"),
    (r"G[UL]+SH[IE]T|GLUSHITEL|GULSHITER|REZONAT", "CAT-EXH-MUF"),
    # Body.
    (r"STEKLOPOD|STEKLOPOD.?YOMN|STEKLAPOD", "CAT-BODY-WIN"),
    (r"KOROMISL|TRAPETS|DVORNIK\w* (MOTOR|MATOR|MEXAN)|MOTOR DVORNIK", "CAT-BODY-WMECH"),
    (r"DVORNIK|SHCHETK|SHETKA STEKL", "CAT-BODY-WIPER"),
    (r"FARA\b|FARA ", "CAT-BODY-HEAD"),
    (r"FONAR\w* ZADN|ZADN\w* FONAR|\bSTOP\b", "CAT-BODY-TAIL"),
    (r"POVOROTN|PAVAROTN|PLAFON|PODFARNIK|GABARIT", "CAT-BODY-LAMP"),
    (r"ZERKAL|KO'ZGU", "CAT-BODY-MIRROR"),
    (r"REZINA|UPLOTNIT", "CAT-BODY-SEAL"),
    ((r"ESHIK|ZAMOK|DUGA|SPINK|FIKSATOR|ZASHCHELK|ZASHELK|RUCHK|ILMOQ|LEGUSHKA|KAPOT|BAGAJ|BAMPER|KRILO|SIDENA|"
     r"PEREDOK|DVER"), "CAT-BODY-OTHER"),
    # Fluids.
    (r"ANTIFRIZ|ANTFRIZ|TOSOL", "CAT-OIL-COOL"),
    (r"KRISHKA BENZ|BENZ\w* BAK", "CAT-FUEL"),
    (r"BACHOK VO[XZ]DU", "CAT-FLT"),
    (r"JIDKOST\w* .*TORMOZ|TORMOZ\w* JIDKOST|\bDOT ?4\b", "CAT-OIL-BRK"),
    (r"MASLO|\b\d{1,2}W-?\d{2}\b", "CAT-OIL-ENG"),
    # Small parts.
    (r"\bBOLT|GAYKA|SHPILKA|SHAYBA|BALON BOLT", "CAT-ACC-FAST"),
    (r"PEDAL|VILKA S[CE]?PLEN", "CAT-DRV-CLKIT"),
    (r"PODSHI[PB]N|PACHIMNIK|\b\d{4,5}-?2?RS\b|\b6[23]\d{2}\b", "CAT-DRV-BRG"),
    (r"\bMODUL\b", "CAT-IGN-MOD"),
    (r"^PALES", "CAT-ENG-PIST"),
    (r"JIDKOST", "CAT-OIL"),
    (r"TROS", "CAT-BODY-OTHER"),
    (r"SHLANG|SHLANK|TRU?PKA|TRUBKA|TRAYNIK", "CAT-COOL-HOSE"),
    (r"FIL+T[EI]?R", "CAT-FLT"),
)
_COMPILED_RULES = tuple((re.compile(pattern), type_id) for pattern, type_id in TYPE_RULES)

# A part type that covers several parts ("Gearbox parts") names the actual part instead.
SUBTYPE_NAMES: dict[str, tuple[tuple[str, tuple[str, str, str]], ...]] = {
    "CAT-ENG-PIST": (
        (r"K[AO]L[TS]?S[AO]|COLSA|CALSO", ("Porshen halqalari", "Кольца поршневые", "Piston rings")),
        (r"PALES|PALETS", ("Porshen barmog'i", "Палец поршневой", "Piston pin")),
        (r"PORSH", ("Porshen", "Поршень", "Piston")),
    ),
    "CAT-ENG-CRSH": (
        (r"SHATUN", ("Shatun", "Шатун", "Connecting rod")),
        (r"", ("Tirsakli val (kolenval)", "Коленвал", "Crankshaft")),
    ),
    "CAT-ENG-VALVE": (
        (r"GI?DRO", ("Gidrokompensator", "Гидрокомпенсатор", "Hydraulic lifter")),
        (r"SUXARIK", ("Klapan suxarigi", "Сухари клапана", "Valve keepers")),
        (r"NAPRAVLYASH", ("Klapan vtulkasi", "Направляющая втулка клапана", "Valve guide")),
        (r"KLAP", ("Klapan", "Клапан", "Valve")),
    ),
    "CAT-ENG-TCHAIN": (
        (r"BASHMAK", ("Zanjir bashmagi", "Успокоитель цепи ГРМ", "Timing chain guide")),
        (r"", ("GRM zanjiri (sep)", "Цепь ГРМ", "Timing chain")),
    ),
    "CAT-ENG-OTHER": (
        (r"KOJUX|ZUBCHAT", ("GRM qopqog'i", "Кожух ГРМ", "Timing belt cover")),
        (r"MATOR KRISHK|MOTOR KRISHK", ("Dvigatel qopqog'i", "Крышка двигателя", "Engine cover")),
        (r"KOL+EKTOR", ("Kollektor", "Коллектор", "Manifold")),
        (r"KARTER", ("Karter (poddon)", "Поддон картера", "Oil pan")),
        (r"SAPUN|SAFUN", ("Sapun", "Сапун", "Crankcase breather")),
        (r"SHKIF", ("Shkiv", "Шкив", "Pulley")),
        (r"ZAGLUSHK", ("Zaglushka", "Заглушка", "Plug")),
        (r"SHUP", ("Moy shchupi", "Щуп масляный", "Oil dipstick")),
        (r"MAXOVIK|VENIS|VENETS", ("Maxovik va venets", "Маховик / венец", "Flywheel & ring gear")),
        (r"ZVOZDOCHK", ("Yulduzcha (zvezdochka)", "Звёздочка", "Sprocket")),
        (r"SHESTERNA", ("Shesternya", "Шестерня", "Gear")),
    ),
    "CAT-ENG-GSK": (
        (r"NABOR", ("Prokladkalar to'plami", "Комплект прокладок", "Gasket set")),
        (r"KARTER|PODDON", ("Karter prokladkasi", "Прокладка поддона", "Oil pan gasket")),
        (r"KOL+EKTOR|KAL+EKTOR", ("Kollektor prokladkasi", "Прокладка коллектора",
                                  "Manifold gasket")),
        (r"", ("Prokladka", "Прокладка", "Gasket")),
    ),
    "CAT-ENG-SEALS": ((r"", ("Salnik", "Сальник", "Oil seal")),),
    "CAT-ENG-TTEN": (
        (r"\bSEP\b|TSEP", ("GRM zanjiri taranglagichi", "Натяжитель цепи ГРМ",
                           "Timing chain tensioner")),
        (r"DINAM|GENERATOR", ("Generator tasmasi roligi", "Натяжитель приводного ремня",
                              "Drive belt tensioner")),
    ),
    "CAT-BRK-VAC": (
        (r"SHLAN", ("Vakuum shlangi", "Вакуумный шланг", "Vacuum hose")),
        (r"KLAP", ("Teskari klapan", "Обратный клапан", "Check valve")),
    ),
    "CAT-EXH-GSK": (
        (r"REZINA", ("Glushitel osmasi (rezina)", "Подвес глушителя", "Exhaust hanger")),
        (r"KOL+EKTOR|KAL+EKTOR|PRIYOMN|PRIEMN", ("Kollektor prokladkasi", "Прокладка коллектора",
                                                "Manifold gasket")),
        (r"XOMUT", ("Glushitel xomuti", "Хомут глушителя", "Exhaust clamp")),
        (r"", ("Glushitel prokladkasi", "Прокладка глушителя", "Exhaust gasket")),
    ),
    "CAT-FUEL-PUMP": (
        (r"SHLAN", ("Benzonasos shlangi", "Шланг бензонасоса", "Fuel pump hose")),
    ),
    "CAT-COOL-THERM": (
        (r"KRISHK|KORPUS", ("Termostat korpusi", "Корпус термостата", "Thermostat housing")),
    ),
    "CAT-DRV-BRG": ((r"", ("Podshipnik", "Подшипник", "Bearing")),),
    "CAT-DRV-SEAL": (
        (r"PEREVECH|VTORICH|KPP|KAR[AO][PB]K", ("KPP salnigi", "Сальник КПП", "Gearbox seal")),
    ),
    "CAT-BRK-CAL": (
        (r"PIL+N", ("Support pilnigi", "Пыльник суппорта", "Caliper boot")),
        (r"PAL[EI]", ("Support barmog'i", "Направляющая суппорта", "Caliper guide pin")),
    ),
    "CAT-FLT": (
        (r"GOFRA|P[AO]T+R?UBK", ("Havo filtri gofrasi", "Гофра воздушного фильтра",
                                 "Air intake hose")),
        (r"BACHOK", ("Havo filtri korpusi", "Корпус воздушного фильтра", "Air filter housing")),
        (r"", ("Filtr", "Фильтр", "Filter")),
    ),
    "CAT-IGN-MOD": (
        (r"KRISHK\w* TRAMBL", ("Trambler qopqog'i", "Крышка трамблёра", "Distributor cap")),
        (r"TRAMBL", ("Trambler", "Трамблёр (распределитель)", "Distributor")),
        (r"BEGUNOK", ("Begunok", "Бегунок трамблёра", "Distributor rotor")),
    ),
    "CAT-FUEL-GAS": (
        (r"PEDAL", ("Gaz pedali", "Педаль газа", "Accelerator pedal")),
        (r"", ("Gaz trosi", "Трос газа", "Accelerator cable")),
    ),
    "CAT-BODY-WMECH": (
        (r"BACHO", ("Oyna yuvish bachogi", "Бачок омывателя", "Washer reservoir")),
        (r"STOYKA|RICHAG|KOROMISL", ("Dvornik richagi", "Рычаг стеклоочистителя", "Wiper arm")),
        (r"MOTOR|MATOR", ("Dvornik motori", "Мотор стеклоочистителя", "Wiper motor")),
    ),
    "CAT-ENG-MOUNT": (
        (r"KRANSHTEYN", ("Dvigatel kronshteyni", "Кронштейн опоры двигателя",
                         "Engine mount bracket")),
    ),
    "CAT-SUS-MOUNT": (
        (r"CHASHKA|OPORA|[AO]PORNIK|PODUSHK", ("Amortizator tayanchi (chashka)",
                                               "Опора амортизатора (чашка)", "Strut mount")),
        (r"PIL+N", ("Amortizator pilnigi", "Пыльник амортизатора", "Shock absorber boot")),
        (r"BOYNIK|LOLA", ("Otboynik", "Отбойник амортизатора", "Bump stop")),
    ),
    "CAT-SUS-BUSH": (
        (r"STAB|STALB|STILB|STAL", ("Stabilizator vtulkasi", "Втулка стабилизатора",
                               "Stabilizer bar bush")),
        (r"RES+OR", ("Ressor vtulkasi", "Втулка рессоры", "Leaf spring bush")),
        (r"", ("Saylentblok (vtulka)", "Сайлентблок (втулка)", "Bush")),
    ),
    "CAT-COOL-HTR": (
        (r"MOTOR|MATOR|VENT|VINT", ("Pechka motori", "Мотор печки", "Heater blower motor")),
        (r"KRAN|KLAP", ("Pechka krani", "Кран печки", "Heater valve")),
        (r"TROS|KLUCH", ("Pechka trosi", "Трос печки", "Heater control cable")),
        (r"SHLAN|TRU?PK|TRUBK|TURUPK|TRAYNIK", ("Pechka shlangi", "Шланг печки", "Heater hose")),
        (r"PANEL|OTOPIT", ("Pechka boshqaruv paneli", "Панель управления отопителем",
                           "Heater control panel")),
    ),
    "CAT-COOL-ACP": (
        (r"DEFIZOR|VENT|VINT", ("Konditsioner ventilyatori", "Вентилятор кондиционера",
                                "A/C condenser fan")),
        (r"RADIATOR", ("Konditsioner radiatori", "Радиатор кондиционера", "A/C condenser")),
        (r"SHLAN|TRU?PK|TRUBK", ("Konditsioner trubkasi", "Трубка кондиционера", "A/C pipe")),
    ),
    "CAT-COOL-TANK": (
        (r"KRISHK", ("Bachok qopqog'i", "Крышка бачка", "Expansion tank cap")),
    ),
    "CAT-STR-OTHER": (
        (r"BACHO", ("GUR bachogi", "Бачок ГУР", "Power steering reservoir")),
        (r"KALONKA|KOLONKA", ("Rul kolonkasi", "Рулевая колонка", "Steering column")),
        (r"MAYATNIK", ("Rul mayatnigi", "Маятник рулевой", "Idler arm")),
        (r"SHLAN|TRU?PK|TRUBK", ("GUR shlangi", "Шланг ГУР", "Power steering hose")),
        (r"PODUSHK|ROLAVOY", ("Rul reykasi yostig'i", "Опора рулевой рейки", "Steering rack mount")),
    ),
    "CAT-EL-SENS": (
        (r"TERMO|TEMPERAT|SUV", ("Harorat datchigi", "Датчик температуры", "Temperature sensor")),
        (r"\bMAP\b|DAVLEN", ("Bosim datchigi (MAP)", "Датчик давления (MAP)", "MAP sensor")),
        (r"MASL", ("Moy bosimi datchigi", "Датчик давления масла", "Oil pressure sensor")),
        (r"BENZ", ("Benzin sathi datchigi", "Датчик уровня топлива", "Fuel level sensor")),
        (r"SKOROS", ("Tezlik datchigi", "Датчик скорости", "Speed sensor")),
        (r"PUSHKA|DETONA", ("Detonatsiya datchigi", "Датчик детонации", "Knock sensor")),
        (r"BALON|SHINA", ("Shina bosimi datchigi", "Датчик давления в шинах",
                          "Tyre pressure sensor")),
        (r"RASP|KOLEN|KALEN|POLOJ", ("Val holati datchigi", "Датчик положения вала",
                                     "Shaft position sensor")),
        (r"", ("Datchik", "Датчик", "Sensor")),
    ),
    "CAT-EL-ALT": (
        (r"SHOTKA|SHCHETK|SHETK", ("Generator cho'tkalari", "Щётки генератора",
                                   "Alternator brushes")),
        (r"DIOD|DIOT", ("Diod ko'prigi", "Диодный мост", "Rectifier")),
        (r"STATOR", ("Generator statori", "Статор генератора", "Alternator stator")),
    ),
    "CAT-EL-START": (
        (r"BEN?D[EI]KS|BINDEKS", ("Bendiks", "Бендикс стартера", "Starter drive")),
        (r"PUSKACH", ("Starter tortuvchi relesi", "Втягивающее реле стартера",
                      "Starter solenoid")),
    ),
    "CAT-EL-SW": (
        (r"STOP", ("Stop-signal tugmasi", "Выключатель стоп-сигнала", "Brake light switch")),
        (r"KNOPK", ("Tugma", "Кнопка", "Button")),
        (r"ZAJIG|\bKLUCH", ("O't oldirish qulfi", "Замок зажигания", "Ignition switch")),
    ),
    "CAT-EL-DASH": (
        (r"TROS", ("Spidometr trosi", "Трос спидометра", "Speedometer cable")),
    ),
    "CAT-EL-RELAY": (
        (r"PAVAROT|POVOROT", ("Burilish relesi", "Реле поворотов", "Turn signal relay")),
        (r"BENZ", ("Benzonasos relesi", "Реле бензонасоса", "Fuel pump relay")),
        (r"GENERATOR|DINAM", ("Generator relesi", "Реле-регулятор генератора",
                              "Alternator regulator")),
        (r"PREDOXRAN|PRIDOXNA|PREDOHRAN", ("Saqlagich", "Предохранитель", "Fuse")),
        (r"", ("Rele", "Реле", "Relay")),
    ),
    "CAT-DRV-GBX": (
        (r"PODSHI", ("KPP podshipnigi", "Подшипник КПП", "Gearbox bearing")),
        (r"MUFT", ("Sinxronizator muftasi", "Муфта синхронизатора", "Synchronizer sleeve")),
        (r"SINXRON|SINHRON", ("Sinxronizator", "Синхронизатор", "Synchronizer")),
        (r"PERVICH|PEREVECH|PEREVISH", ("Birlamchi val", "Первичный вал КПП", "Input shaft")),
        (r"VTORICH", ("Ikkilamchi val", "Вторичный вал КПП", "Output shaft")),
        (r"KUL[IY][SC]A", ("Kulisa", "Кулиса КПП", "Gear shift linkage")),
        (r"VILKA", ("KPP vilkasi", "Вилка КПП", "Shift fork")),
        (r"FIL+T", ("KPP filtri", "Фильтр КПП", "Transmission filter")),
        (r"SHESTERNA", ("KPP shesternyasi", "Шестерня КПП", "Gearbox gear")),
        (r"QUYON|PRUJ", ("KPP prujinasi", "Пружина КПП", "Gearbox spring")),
    ),
    "CAT-DRV-CLKIT": (
        (r"K[AO]RZIN", ("Ilashish savati (korzina)", "Корзина сцепления",
                        "Clutch pressure plate")),
        (r"DISK", ("Ilashish diski", "Диск сцепления", "Clutch disc")),
        (r"VILKA", ("Ilashish vilkasi", "Вилка сцепления", "Clutch fork")),
        (r"PEDAL", ("Pedal", "Педаль", "Pedal")),
    ),
    "CAT-DRV-CLCYL": (
        (r"GL[AO]VN|GILAVNI", ("Ilashish bosh silindri", "Главный цилиндр сцепления",
                               "Clutch master cylinder")),
        (r"RABOCH", ("Ilashish ishchi silindri", "Рабочий цилиндр сцепления",
                     "Clutch slave cylinder")),
    ),
    "CAT-DRV-SHAFT": (
        (r"KARDAN|KR[IE]STOV|KIRISTAV", ("Kardan va krestovina", "Кардан и крестовина",
                                         "Propeller shaft & U-joint")),
    ),
    "CAT-BODY-SEAL": (
        (r"ESHIK|DVER", ("Eshik rezinasi", "Уплотнитель двери", "Door seal")),
        (r"BAGAJ", ("Bagaj rezinasi", "Уплотнитель багажника", "Boot seal")),
        (r"G[UL]+SH", ("Glushitel rezinasi", "Подвес глушителя", "Exhaust hanger")),
    ),
    "CAT-BODY-OTHER": (
        (r"RUCHK", ("Dastak (ruchka)", "Ручка", "Handle")),
        (r"ZAMOK|ZASH|LEGUSHKA|ILMOQ", ("Qulf", "Замок", "Lock")),
        (r"TROS", ("Tros", "Трос", "Cable")),
        (r"SIDENA|SPINK", ("O'rindiq mexanizmi", "Механизм сиденья", "Seat mechanism")),
        (r"AMORT", ("Bagaj amortizatori", "Амортизатор багажника", "Boot gas strut")),
    ),
    "CAT-BODY-LAMP": (
        (r"POVOROT|PAVAROT", ("Burilish chirog'i", "Поворотник", "Turn signal lamp")),
        (r"PLAFON", ("Plafon", "Плафон", "Interior lamp")),
    ),
    "CAT-ACC-FAST": (
        (r"GAYKA", ("Gayka", "Гайка", "Nut")),
        (r"SHPILKA", ("Shpilka", "Шпилька", "Stud")),
        (r"", ("Bolt", "Болт", "Bolt")),
    ),
}
_COMPILED_SUBTYPES = {
    type_id: tuple((re.compile(pattern), names) for pattern, names in entries)
    for type_id, entries in SUBTYPE_NAMES.items()
}

# Rear drum brakes are shoes on these cars; the bigger ones have rear discs and pads.
REAR_DISC_MODELS = re.compile(r"LACETTI|LASETTI|GENTRA|CAPTIVA|KAPTIVA|MALIBU|EPICA|CRU[ZS]|ORLANDO|"
                              r"TRACKER|EQUINOX")

_FRONT = re.compile(r"\b(OLDI\w*|OLD|PEREDN\w*|PERED|FRONT)\b")
_REAR = re.compile(r"\b(ORQA|ORKA|ZADN\w*|REAR)\b")
_LEFT = re.compile(r"\b(LH|CHAP|LEV\w*|LEFT)\b|(?<=\d)-?L\b|-L\b|\bL\)")
# "PRAVODA" is a wire ("провода"), not "правый".
_RIGHT = re.compile(r"\b(RH|O'?NG|PRAV(?![AO]D)\w*|RIGHT)\b|(?<=\d)-?R\b|-R\b|\bR\)")
_OUTER = re.compile(r"\b(TASHQI|TASHKI|NARUJ\w*|OUTER)\b")
_INNER = re.compile(r"\b(ICHKI|VNUTR\w*|INNER)\b")
# Repair sizes of pistons, rings, liners and bearing shells: STD, 0.25, 0,50, 025, 050.
_SIZE = re.compile(r"\bSTD\b|(?<![\d.,])(?:0[.,]?)?(25|50|75)\b|\b1[.,]00\b")
SIZED_TYPES = {"CAT-ENG-PIST", "CAT-ENG-BRG", "CAT-ENG-LINER", "CAT-ENG-CRSH"}

# Words worth keeping in the clean name, in Uzbek, Russian and English.
DESCRIPTORS: tuple[tuple[str, tuple[str, str, str]], ...] = (
    (r"\b(ZB[OA]R\w*|SBOR\w*|YIG'ILGAN|KOMPLEKT)\b", ("yig'ilgan", "в сборе", "assembly")),
    (r"\bKATTA\b|\bKOTTA\b|\bBOLSH\w*", ("katta", "большой", "large")),
    (r"\bKICHIK\b|\bMAL\w*\b", ("kichik", "малый", "small")),
    (r"\bUZUN\b|\bDLIN\w*", ("uzun", "длинный", "long")),
    (r"\bKALTA\b|\bKOROTK\w*", ("kalta", "короткий", "short")),
    (r"\bTEMIR\w*|\bMETAL\w*|\bALUMEN\w*", ("metall", "металлический", "metal")),
    (r"\bPLAS\w*", ("plastik", "пластиковый", "plastic")),
    (r"\bPREMIUM\b", ("Premium", "Премиум", "Premium")),
    (r"\bA/?T\b|\bAKPP\b", ("AT", "АКПП", "automatic")),
    (r"\bM/?T\b|\bMKPP\b", ("MT", "МКПП", "manual")),
    (r"\b(16V|16 KL\w*|DOHC)\b", ("DOHC", "DOHC", "DOHC")),
    (r"\b(8V|SOHC)\b", ("SOHC", "SOHC", "SOHC")),
)
_DESCRIPTORS = tuple((re.compile(pattern), names) for pattern, names in DESCRIPTORS)

POSITION_WORDS = {
    "front": ("oldi", "пер.", "front"),
    "rear": ("orqa", "зад.", "rear"),
    "left": ("chap", "лев.", "left"),
    "right": ("o'ng", "прав.", "right"),
    "outer": ("tashqi", "наруж.", "outer"),
    "inner": ("ichki", "внутр.", "inner"),
}

# Part numbers: GM (96273708, P96133096, 96445372R), Suzuki-built Damas/Tico (74120A78B00,
# 11141A78B00-000), Hyundai/Kia (54300-4E400), CTR (CBKD-14), bearings (6203-RS) and the
# seller's own codes (NP1013).
_NUMBER_PATTERNS = (
    re.compile(r"\b\d{5}[A-Z]\d{2}[A-Z0-9]\d{2}(?:-\d{3})?\b"),
    re.compile(r"\b\d{5}-\d{5}(?:-\d{3})?\b"),
    re.compile(r"\b\d{5}-[0-9A-Z]{5}\b"),
    re.compile(r"\bC[BREQT][A-Z]{2}-?\d{1,3}[RL]?\b"),
    re.compile(r"\b[A-Z]{1,3}-?\d{4,6}(?:-[A-Z0-9]{1,4})?\b"),
    re.compile(r"(?<![\d.,])P?\d{6,10}(?:/\d{1,8})*[A-Z]{0,2}(?![\d.,])"),
)
_GM_RUN = re.compile(r"^P?(\d{6,10})((?:/\d{1,8})*)[A-Z]{0,2}$")


def part_numbers(text: str) -> list[str]:
    """Every part number in the text, "96267421/22/23/24" expanded to four numbers."""
    value = latin_upper(text)
    found: list[str] = []
    taken: list[tuple[int, int]] = []
    for pattern in _NUMBER_PATTERNS:
        for match in pattern.finditer(value):
            if any(start < match.end() and match.start() < end for start, end in taken):
                continue
            taken.append(match.span())
            token = match.group()
            run = _GM_RUN.match(token)
            if run:
                first, rest = run.groups()
                found.append(first)
                for tail in filter(None, rest.split("/")):
                    found.append(tail if len(tail) >= len(first) else first[: -len(tail)] + tail)
            elif sum(char.isdigit() for char in token) >= 4:
                found.append(token)
    return list(dict.fromkeys(found))


def _spec_tokens(value: str, numbers: list[str]) -> list[str]:
    """Codes that tell parts apart but are not part numbers: 5PK1008, RN9YC, 6203-RS."""
    specs = []
    for token in re.findall(r"[A-Z0-9][A-Z0-9-]*", value):
        if token in numbers or not any(char.isdigit() for char in token):
            continue
        if re.fullmatch(r"\d+(SHT|M|KM|OY|TA)", token) or token in {"16V", "8V"}:
            continue
        if any(char.isalpha() for char in token) and len(token) >= 4:
            specs.append(token)
    return [spec for spec in dict.fromkeys(specs) if not any(spec in number for number in numbers)]


@dataclass
class PartName:
    type_id: str | None
    position: str | None = None
    side: str | None = None
    placement: str | None = None
    size: str | None = None
    numbers: list[str] = field(default_factory=list)
    descriptors: list[tuple[str, str, str]] = field(default_factory=list)
    specs: list[str] = field(default_factory=list)
    cleaned: str = ""
    # The actual part within a broad type ("Synchronizer" within "Gearbox parts").
    subtype: tuple[str, str, str] | None = None

    def key(self) -> tuple:
        return (self.subtype or self.type_id or self.cleaned, self.position, self.side, self.placement, self.size,
                tuple(names[0] for names in self.descriptors), tuple(self.specs))


def read_part_name(raw: str, model_text: str = "") -> PartName:
    value = latin_upper(raw)
    numbers = part_numbers(raw)
    type_id = next((type_id for pattern, type_id in _COMPILED_RULES if pattern.search(value)), None)
    rear_discs = bool(REAR_DISC_MODELS.search(latin_upper(model_text)))
    if type_id == "CAT-BRK-PAD" and _REAR.search(value) and not rear_discs:
        type_id = "CAT-BRK-SHOE"
    elif type_id == "CAT-BRK-SHOE" and rear_discs and "BARABAN" not in value:
        type_id = "CAT-BRK-PAD"

    without_numbers = value
    for number in numbers:
        without_numbers = without_numbers.replace(number, " ")
    position = "front" if _FRONT.search(value) else "rear" if _REAR.search(value) else None
    side = "left" if _LEFT.search(value) else "right" if _RIGHT.search(value) else None
    placement = "outer" if _OUTER.search(value) else "inner" if _INNER.search(value) else None
    size = None
    if type_id in SIZED_TYPES and (match := _SIZE.search(without_numbers)):
        size = "STD" if match.group() == "STD" else f"0.{match.group(1)}" if match.group(1) else "1.00"
    descriptors = [names for pattern, names in _DESCRIPTORS if pattern.search(without_numbers)]
    specs = _spec_tokens(without_numbers, numbers) if type_id else []
    cleaned = " ".join(re.sub(r"[()]", " ", without_numbers).split())
    subtype = next(
        (names for pattern, names in _COMPILED_SUBTYPES.get(type_id, ()) if pattern.search(value)),
        None,
    )
    return PartName(
        type_id, position, side, placement, size, numbers, descriptors, specs, cleaned, subtype
    )


def display_names(part: PartName, type_names: tuple[str, str, str] | None) -> tuple[str, str, str]:
    """The part's name in Uzbek, Russian and English."""
    if type_names is None:
        # An unrecognized part keeps the seller's wording, in Cyrillic for Russian readers.
        words = re.sub(r"\b(STD|PREMIUM)\b", " ", part.cleaned).strip(" -/.,") or part.cleaned
        uz = words.capitalize()
        return uz, cyrillic(words).capitalize(), uz

    marks = [mark for mark in (part.position, part.side, part.placement) if mark]
    extra = [*part.descriptors]
    names = []
    for index, base in enumerate(part.subtype or type_names):
        qualifiers = [POSITION_WORDS[mark][index] for mark in marks]
        details = [names_[index] for names_ in extra if names_[index].lower() not in base.lower()]
        tail = " ".join([*qualifiers, *details])
        if index == 1:
            name = f"{base} {tail}".strip()
        else:
            name = f"{base}, {tail}" if tail else base
        tokens = [token for token in (part.size, *part.specs) if token]
        names.append(" ".join([name, *tokens]))
    return names[0], names[1], names[2]
