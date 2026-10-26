# Product blueprint: status in the code

How the site follows *AutoParts Platform — Yagona product blueprint va qabul qilingan qarorlar*
(24 October 2026). Update this file when a decision changes, as the blueprint asks.

## The 20 decisions

| # | Decision | Status | Where |
|---|---|---|---|
| 1 | Search/sourcing first, not a marketplace | Done. Home page: "find who has the part" for shops, services and mechanics; no payment or checkout | `app/static/index.html`, `app.js` strings |
| 2 | Supplier ≠ Brand | Done | `suppliers`, `brands` tables |
| 3 | Product ≠ Offer | Done | `products`, `supplier_offers` |
| 4 | Supplier code ≠ OEM | Done. Reference types `OE`, `AFTERMARKET` (maker's article), `SUPPLIER_SKU` (seller's code, never joins parts). Every part shows its OEM code or "not known yet"; staff fill the gaps at `/admin/oem`, buyers can send codes for staff to check | `app/price_list_import.py` `reference_type()`, `app/oem.py` |
| 5 | One product → many vehicles | Done | `fitments` |
| 6 | One product → many references | Done | `reference_numbers` |
| 7 | Article is not a unique key | Done. Position, side, repair size and outer/inner are part of identity; a missing one is not a conflict; collisions go to review | `app/catalog.py` `VARIANT_ATTRIBUTES` |
| 8 | Category-specific attributes | Done. Sellers' names fill `position`, `side`, `repair_size`, `placement`, `transmission`, `engine_type`, `spec_code`; shown on the part page | `product_attributes`, `category_attributes` |
| 9 | Weak fuzzy merge is a suggestion only | Done. Parts without a number are never joined across sellers; a review item suggests it | `catalog_review_items`, `/admin/catalog` "Open review items" |
| 10 | Raw source is kept | Done. Every row with file, import batch, match status (`NEW_PRODUCT` / `MATCHED_AUTO`) | `raw_supplier_products` |
| 11 | Multilingual search | Done. Uzbek, Russian, English, translit, keyboard layout, sellers' slang | `app/vocabulary.py`, `app/part_names.py` |
| 12 | Exact code is priority #1 | Done. `PT43` = `PT 43`; reference and seller-code matches rank first | `app/search.py` |
| 13 | RELATED kept apart | Done. Shown under "similar results", in cards and in the table view | `app.js` `renderResults` |
| 14 | Analytics on normalized queries | Done (pilot mode) | `app/analytics.py` |
| 15 | Stock/price is not identity | Done. Only on offers | `supplier_offers` |
| 16 | Freshness matters | Done. Order: stock → freshness → preferred supplier → price → reliability → hand-over time | `app/offers.py` `offer_sort_key` |
| 17 | Payment/delivery later | Kept out. Reservation and basket only | — |
| 18 | Credit risk not on the platform | Kept out | — |
| 19 | Real supplier pilot | Started. KOREA, WEISMO, BOS-KOS and "BIZDA BOR" lists imported; Megaparts (IRIZON) workbook earlier | `app/price_list_import.py` |
| 20 | Moat = data graph | Building. Cross-supplier audit (CONFIRMED / PROBABLE), demand without supply in analytics | `product_audits`, `app/analytics.py` |

## Roadmap stages

| Stage | Status |
|---|---|
| 0. Catalog foundation | Done: importer for any seller layout, review queue, cross-supplier audit |
| 1. Search MVP | Done: synonyms, typo tolerance, EXACT / COMPATIBLE / RELATED |
| 2. Analytics / pilot | Built (pilot mode); needs 10–20 real users |
| 3. Supplier offers | Done: price, stock, freshness, seller cards, call / Telegram / reserve, basket across sellers |
| 4. Real sync | Excel upload works (`/admin/suppliers`); scheduled sync and 1C/API need sellers' access |
| 5. RFQ + demand intelligence | Part requests and seller applications reach staff; suppliers answering needs a supplier panel |
| 6. Commercial terms | Not started (needs sellers' individual prices and limits) |
| 7. Later (VIN depth, B2C, delivery, payment) | Not started by design |

## Open questions (need the business)

- Seller names and contacts for the "BIZDA BOR", "KOREA" and "YANGI WEISMO" lists; whether KOREA and YANGI WEISMO are one seller.
- "BIZDA BOR" prices (`NARXI`, worked out from yuan, in dollars): wholesale or retail, and shown in dollars or so'm.
- BOS-KOS `KAROBKA` column: pieces per carton, or stock.
- Brands `IM`, `OEM` and `UZ-DAEWOO`: what each means for quality (original, factory supplier, aftermarket).
- Unrecognised words: KULACHOK, ELEMENT, STAKAN, NAY, ABOYMA; and which car "LACETTI GB" is.
- Megaparts real stock and price export (blueprint P0).
- A source for the OEM codes still missing (about a third of parts): sellers adding an OEM
  column to their lists, a parts-catalog program staff use, or a licensed catalog (TecDoc).
