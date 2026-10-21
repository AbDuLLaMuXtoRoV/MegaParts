# MegaParts catalog backend

PostgreSQL + FastAPI backend for the audited auto-parts workbook. It keeps brands and
suppliers separate, models all catalog many-to-many relationships, and quarantines master
products whose cross-supplier audit status is `CONFLICT`.

## Run locally

```bash
cp .env.example .env
docker compose up -d postgres
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
alembic upgrade head
catalog-import 'IRIZON_Master_Catalog_v2.0 (1).xlsx'
uvicorn app.main:app --reload
```

The active master source is `IRIZON_Master_Catalog_v2.0 (1).xlsx`. Catalog workbooks are
private business data and are not in this repository; put the workbook in the project folder
before importing (the workbook-based tests skip without it). Re-import atomically
with `catalog-import <workbook> --replace`. The importer auto-detects the IRIZON v2 schema
while retaining compatibility with the original audited workbook. Without `--replace`, the
command refuses to modify a populated catalog.

Search examples:

```bash
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'q=PT 43'
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'q=94544449'
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'q=Nexia 3 amortizator'
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'q=Cobalt ABS oldi LH'
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'q=Spark benzin nasos'
```

`oldi`, `orqa`, `LH`, `RH`, `передний`, and `задний` are normalized to canonical
position/side terms. Code normalization ignores spacing and punctuation, so `PT43` and
`PT 43` are equivalent.

Search parses product, vehicle, brand, reference, position, and side as independent intents.
The configurable vocabulary lives in `app/search_vocabulary.py`; it expands Cyrillic,
Latin/transliterated product names and common vehicle aliases without rewriting catalog data.
Every catalog model name (for example `nexia` → Daewoo Nexia) is also recognized as a
vehicle automatically; models shorter than four characters (`K5`, `X70`) are skipped as too
ambiguous.

### Typo tolerance

Customers find parts even when they misspell them. Before any correction, search already
accepts:

- Uzbek apostrophes in any form or none (`yoqilgi`, `yoqilgʻi`, `yoqilg'i`), and `ё` as `е`.
- Words in any order (`масляный фильтр` finds "Фильтр масляный").
- Part-type names in all three languages (`шрус`, `катушка зажигания`).
- Filler words in a sentence (`Cobalt uchun svecha kerak`, `нужны колодки для кобальт`).
  The list is `STOP_WORDS` in `app/search_vocabulary.py`.

When a query word is not a catalog word or prefix, `app/vocabulary.py` corrects it:

- **Typos:** 1 edit for words up to 5 letters, 2 for longer; transpositions count as one
  (`amortizatr`, `brake pda`).
- **Spelling by ear:** words that sound alike: Uzbek h/x and q/k, transliteration, unstressed
  о/а and е/и, voiced/voiceless pairs (`neksiya` → `nexia`, `kalotki` → `kolodka`,
  `амартизатор`).
- **Misspelled start of a longer word:** `salnek` → `salnigi`.
- **Words run together:** `moyfiltri` → `moy filtri`.
- **Wrong keyboard layout:** `cdtxf` → `свеча`, `лщдщвлф` → `kolodka`.

Each word keeps a few likely fixes, and search tries the resulting queries in order. It
keeps the first one that finds parts, so a plausible but useless fix gives way to the next.
Only if no fix finds anything are words the catalog has never seen left out
(`kolodka brembo` → `kolodka`).

A correction is used only when the original spelling found no exact or compatible match.
The response then carries `corrected_query`, and the page shows what was searched. Words with
digits and words under three letters are never corrected. Pass `spellcheck=false` to search
the literal spelling; the page offers this as "Search for exactly that". Analytics record what
the customer typed, not the correction.

`GET /api/v1/suggest?q=` powers the list under the search box. It returns the spelling fix,
matching part types with counts, and top parts, and accepts the same car parameters as search.
Suggestions are not recorded in analytics.

### Search by car

`GET /api/v1/vehicles` lists cars that have at least one searchable fitted part. Search accepts
`make`, `make` + `model`, or `vehicle_id` (one generation), and `q` may be empty to list every
part for that car:

```bash
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'make=Chevrolet' --data-urlencode 'model=Cobalt'
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'q=svecha' --data-urlencode 'make=Chevrolet' --data-urlencode 'model=Cobalt'
```

A vehicle typed into `q` overrides the selected car. The catalog page remembers the chosen car
per browser.

### Browse by part type

The catalog page lets customers pick their car, then a part group (Engine, Brakes,
Suspension, …) and a part type, or type a search and narrow the results by part type. It is
available in Uzbek, Russian and English and has a larger-text switch.

`GET /api/v1/part-groups` lists every group with its part types and searchable part counts;
pass `make`/`model`/`vehicle_id` to count only parts that fit that car. Search accepts
`category` (a group or a type) and allows an empty `q` with it:

```bash
curl --get 'http://localhost:8000/api/v1/search' --data-urlencode 'category=CAT-BRK' --data-urlencode 'make=Chevrolet'
```

Search responses include `category_counts` (matches per part type). Parts marked `universal`
(chemicals, tools, bulbs) count as fitting every car when a car is chosen.

The workbook's Categories sheet stays the source of truth. `app/part_types.py` adds the
standard mechanical part types the workbook does not define yet (brake discs, clutch kit,
timing belt, …) so customers can browse the whole car; the importer and migration
`20261021_0008` add only the missing ones and never overwrite workbook rows. Add products
to these types from `/admin/catalog`.

### Admin search vocabulary

`/admin/search-analytics` has a “Teach search a new word” panel and a Fix button on zero-result
queries. An alias maps a customer word to a part concept or a car; the target must already
exist in the vocabulary or the catalog. Aliases take effect on the next search.

- `GET /api/admin/search-aliases`, `POST /api/admin/search-aliases`,
  `DELETE /api/admin/search-aliases/{id}`
- `GET /api/admin/search-aliases/targets` (suggested part concepts and cars)

Set `SEARCH_DEBUG=true` only in development to include parsed intent and per-result score
components in API responses. Production responses omit `search_debug`.

## Data integrity decisions

- `SUPPLIER_INTERNAL_CODE` rows are deliberately excluded from `reference_numbers`.
  They remain searchable through `supplier_offers.supplier_sku` and are retained verbatim
  in `raw_supplier_products`.
- Every source row is retained in `raw_supplier_products` with audit status/reason and its
  source payload.
- Products marked `CONFLICT` remain linked for investigation but have
  `products.is_searchable = false`; the public search API never returns them.
- The API exposes catalog search only. Checkout, payment, and delivery are outside scope.

OpenAPI documentation is available at `http://localhost:8000/docs`.

## Full workbook import

`catalog-import` loads every data sheet of the IRIZON v2 workbook: brands, categories and
category attributes, products (uz/ru/en names, specs, EAN, status), product attributes,
references, vehicles (years, engine, body, fuel, power…), fitments (position, side, quantity,
confidence…), suppliers, supplier offers, search synonyms, supersessions, kits, media, the
review queue, cross-supplier audit findings (the Merge Conflicts sheet is its CONFLICT subset),
settings, the Lists sheet (form dropdowns), and the Data Dictionary (form help text).
Spreadsheet formula columns (`AVTO (formula)` in the Data Dictionary) are recomputed, not
stored. Search synonyms feed search, so Cyrillic vehicle names such as `Тико` or `Кобальт`
are recognized.

## IRIZON profile (catalog editor)

After signing in, `/admin/catalog` shows the supplier profile and the full catalog. Every
product opens as a form with all workbook fields, category-specific attributes, reference
numbers, vehicle fitments, and supplier offers. Saving validates against the workbook's Lists,
updates search immediately, and refuses stale edits (`409`) when the product changed after it
was opened. Prices or stock typed into an offer mark it `LIVE`; removing an offer deactivates it
so reservations keep working. Status other than `ACTIVE` hides a product from search.

## Admin login

Every `/admin/*` page and `/api/admin/*` endpoint requires signing in at `/admin/login`.
Signed-out pages redirect to the login form and APIs return `401`. Configure the account in
`.env`:

```bash
ADMIN_USERNAME=irizon
ADMIN_PASSWORD=<long random password>
SESSION_SECRET=<long random string>   # keeps admins signed in across restarts
SECURE_COOKIES=true                   # when served over HTTPS
```

Admin stays locked until `ADMIN_PASSWORD` is set. Sessions last 12 hours
(`ADMIN_SESSION_HOURS`) in an HttpOnly, SameSite=Lax cookie; changing the password signs
everyone out. Five failed logins from one address lock that address out for 15 minutes.
Restart the server after editing `.env`.

## Pilot mode and search analytics

Set `PILOT_MODE=true` to record search quality events, show the post-click Uzbek feedback
controls, and enable the admin dashboard:

```bash
PILOT_MODE=true uvicorn app.main:app --port 8001
```

The dashboard is available at `http://localhost:8001/admin/search-analytics`. It includes
today, 7-day, 30-day, and custom date ranges. “Needs Catalog Work” flags zero-result
queries, negative feedback, repeated searches without a product click, and queries averaging
at least 50 results without a click.

Pilot endpoints:

- `POST /api/search-events`
- `POST /api/search-events/{id}/click`
- `POST /api/search-events/{id}/action`
- `POST /api/search-events/{id}/feedback`
- `GET /api/admin/search-analytics`

When pilot mode is disabled, search behavior is unchanged, events are not written, feedback
is hidden, and pilot/admin endpoints return `404`.

## Supplier offers v1

Product search and detail responses contain freshness-ranked `offers`. Ranking prefers
available stock, then fresh data, configured preferred suppliers, and finally lower price.
Configure freshness with `OFFER_FRESH_HOURS` / `OFFER_RECENT_HOURS` and preferred supplier
IDs with `PREFERRED_SUPPLIER_IDS=1,2`.

- Supplier pages: `/suppliers/{supplier_id}`
- Supplier admin and XLSX upload: `/admin/suppliers`
- Import history: `/admin/supplier-imports`
- Reservation request: `POST /api/v1/reservations`

Supplier XLSX files must include a `supplier_sku` (or `sku`, `supplier code`, `article`,
`code`) column. Price, stock, warehouse, currency, brand, and reference are optional.
Confirmed supplier-SKU mappings and exact brand/reference matches can update or create an
offer. Unmatched rows are retained in the review queue and never create Master Products.
Existing catalog prices and stock are labeled `DEMO`; imported supplier availability is
labeled `LIVE`. Reservations are lightweight contact requests only—there is no checkout,
payment, or delivery workflow.

## Public demo (Render + Neon)

The demo runs on Render's free web service with a free Neon Postgres database (Render's own
free database is deleted after 30 days; Neon's does not expire).

1. Create a Neon project in AWS Europe (Frankfurt) and copy its connection string.
2. Load the catalog into it from a machine that has the workbook:

   ```bash
   DATABASE_URL='<neon connection string>' alembic upgrade head
   DATABASE_URL='<neon connection string>' catalog-import 'IRIZON_Master_Catalog_v2.0 (1).xlsx'
   ```

3. In Render, choose New > Blueprint, pick this repository, and enter `DATABASE_URL` and
   `ADMIN_PASSWORD` when asked. `render.yaml` sets up the rest.

Free Render services sleep after 15 idle minutes, so the first visit after a pause takes
about a minute. `postgresql://` connection strings are accepted as-is.

## Test

```bash
pytest
```
