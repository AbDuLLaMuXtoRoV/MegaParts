"""Indexable part pages and a sitemap, so a part number typed into Google or Yandex lands here.

Each /part/{id} serves the normal catalog page with the part's own title, description,
schema.org Product data and a plain-HTML summary for crawlers that do not run JavaScript.
"""

from __future__ import annotations

import json
import re
from html import escape
from urllib.parse import quote

from app.schemas import ProductDetail


def part_url(base_url: str, product_id: str) -> str:
    return f"{base_url.rstrip('/')}/part/{quote(product_id, safe='')}"


def _cars(product: ProductDetail) -> list[str]:
    return list(
        dict.fromkeys(
            " ".join(filter(None, [fit.vehicle.make, fit.vehicle.model, fit.vehicle.generation]))
            for fit in product.vehicle_fitments
        )
    )


# The carmaker's (OEM) number first, a seller's own code last.
_NUMBER_ORDER = ("OE", "OES", "AFTERMARKET", "EAN", "SUPPLIER_SKU")


def _numbers(product: ProductDetail) -> list[str]:
    ranked = sorted(
        product.reference_numbers,
        key=lambda ref: _NUMBER_ORDER.index(ref.type) if ref.type in _NUMBER_ORDER else 99,
    )
    return [ref.number for ref in ranked]


def _structured_data(product: ProductDetail, url: str) -> dict:
    data: dict = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "sku": product.id,
        "url": url,
    }
    if product.reference_numbers:
        data["mpn"] = _numbers(product)[0]
    if product.brand:
        data["brand"] = {"@type": "Brand", "name": product.brand.name}
    if product.category:
        data["category"] = product.category.name_en or product.category.name_uz
    cars = _cars(product)
    if cars:
        data["isAccessoryOrSparePartFor"] = [
            {"@type": "Vehicle", "name": car} for car in cars[:20]
        ]
    priced = [offer for offer in product.offers if offer.price is not None]
    if priced:
        in_stock = any((offer.stock_qty or 0) > 0 for offer in product.offers)
        data["offers"] = {
            "@type": "AggregateOffer",
            "priceCurrency": priced[0].currency,
            "lowPrice": str(min(offer.price for offer in priced)),
            "highPrice": str(max(offer.price for offer in priced)),
            "offerCount": len(priced),
            "availability": "https://schema.org/" + ("InStock" if in_stock else "BackOrder"),
        }
    return data


def part_page(template: str, product: ProductDetail, base_url: str) -> str:
    url = part_url(base_url, product.id)
    numbers = ", ".join(_numbers(product)[:5])
    oem = [ref.number for ref in product.reference_numbers if ref.type in ("OE", "OES")]
    cars = _cars(product)
    brand = product.brand.name if product.brand else None
    title = " · ".join(filter(None, [product.name, brand, numbers.split(", ")[0] or None]))
    description = " ".join(
        filter(
            None,
            [
                f"{product.name}{f' ({brand})' if brand else ''}.",
                f"OEM: {', '.join(oem[:3])}." if oem else None,
                f"Raqamlar / номера: {numbers}." if numbers else None,
                f"Mos keladi / подходит: {', '.join(cars[:6])}." if cars else None,
                f"Sotuvchilar: {len(product.offers)}." if product.offers else None,
            ],
        )
    )
    json_ld = json.dumps(_structured_data(product, url), ensure_ascii=False).replace("</", "<\\/")
    head = (
        f'<link rel="canonical" href="{escape(url)}">\n'
        f'    <meta property="og:title" content="{escape(title)}">\n'
        f'    <meta property="og:description" content="{escape(description)}">\n'
        f'    <meta property="og:url" content="{escape(url)}">\n'
        f'    <script type="application/ld+json">{json_ld}</script>\n'
        "  </head>"
    )
    summary = (
        "<noscript><article>"
        f"<h1>{escape(product.name)}</h1>"
        + (f"<p>{escape(brand)}</p>" if brand else "")
        + (f"<p>{escape(numbers)}</p>" if numbers else "")
        + (
            "<ul>" + "".join(f"<li>{escape(car)}</li>" for car in cars) + "</ul>"
            if cars
            else ""
        )
        + "</article></noscript>"
    )
    page = re.sub(r"<title>.*?</title>", f"<title>{escape(title)} — MegaParts</title>", template)
    page = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{escape(description)}">',
        page,
    )
    page = page.replace("</head>", head, 1)
    return re.sub(r"(<body[^>]*>)", lambda match: match.group(1) + summary, page, count=1)


def sitemap(base_url: str, entries: list[tuple[str, str | None]]) -> str:
    """entries: (product id, last-modified ISO date or None)."""
    urls = [f"  <url><loc>{escape(base_url.rstrip('/'))}/</loc></url>"]
    for product_id, modified in entries:
        lastmod = f"<lastmod>{modified}</lastmod>" if modified else ""
        urls.append(f"  <url><loc>{escape(part_url(base_url, product_id))}</loc>{lastmod}</url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def robots(base_url: str) -> str:
    return (
        "User-agent: *\n"
        "Disallow: /admin\n"
        "Disallow: /api/admin\n"
        f"Sitemap: {base_url.rstrip('/')}/sitemap.xml\n"
    )
