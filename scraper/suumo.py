from __future__ import annotations

import logging
import re
from typing import Iterable, List

from bs4 import BeautifulSoup

from .base import parse_float, parse_int, parse_yen
from .models import Property

logger = logging.getLogger(__name__)

# SUUMO の実ページに合わせた代表的なセレクタ。
LISTING_SELECTOR = "div.cassetteitem"
ROOM_ROW_SELECTOR = "table.cassetteitem_other tbody tr"
TITLE_SELECTOR = ".cassetteitem_content-title a, .cassetteitem_content-title"
ADDRESS_SELECTOR = ".cassetteitem_detail-col1"
STATION_TEXT_SELECTOR = ".cassetteitem_detail-col2 li, .cassetteitem_detail-col2 .cassetteitem_detail-text"
BUILDING_INFO_SELECTOR = ".cassetteitem_detail-col3 span, .cassetteitem_detail-col3 div, .cassetteitem_detail-col3"
RENT_SELECTOR = ".cassetteitem_price--rent"
MANAGEMENT_SELECTOR = ".cassetteitem_price--administration"
AREA_SELECTOR = ".cassetteitem_other-area, .cassetteitem_menseki"
FLOOR_SELECTOR = ".cassetteitem_other-floor, .cassetteitem_other-emphasis"
ROOM_LINK_SELECTOR = ".cassetteitem_other-linktext a, .cassetteitem_other-link a, .js-cassetLinkHref"


def parse_list_page(html_soup: BeautifulSoup) -> List[Property]:
    properties: List[Property] = []
    for listing_index, listing in enumerate(html_soup.select(LISTING_SELECTOR)):
        base_title, base_url = _title_and_url(listing.select_one(TITLE_SELECTOR))
        address = _text(listing.select_one(ADDRESS_SELECTOR))
        station_texts = _nonempty_texts(listing.select(STATION_TEXT_SELECTOR))
        nearest_station = station_texts[0] if station_texts else ""
        walk_min = _parse_walk_minutes(nearest_station)

        building_info = " / ".join(_nonempty_texts(listing.select(BUILDING_INFO_SELECTOR)))
        age_year = parse_int(building_info)
        structure = building_info

        rows = listing.select(ROOM_ROW_SELECTOR) or [listing]
        for row_index, row in enumerate(rows):
            try:
                rent_yen = parse_yen(_text(row.select_one(RENT_SELECTOR)))
                management_fee_yen = parse_yen(_text(row.select_one(MANAGEMENT_SELECTOR)))
                area_m2 = parse_float(_text(row.select_one(AREA_SELECTOR)))
                floor_text = _text(row.select_one(FLOOR_SELECTOR))
                floor = parse_int(floor_text)
                room_age_text = _text(row.select_one(".cassetteitem_other-age"))
                room_age_year = parse_int(room_age_text) if room_age_text else age_year
                room_structure = _text(row.select_one(".cassetteitem_other-structure")) or structure

                room_url = _href(row.select_one(ROOM_LINK_SELECTOR)) or base_url
                room_title = base_title or _text(row.select_one(TITLE_SELECTOR))

                property_id = _derive_id(listing, row_index, room_url, room_title, listing_index)

                properties.append(
                    Property(
                        id=property_id,
                        title=room_title,
                        url=room_url,
                        address=address,
                        nearest_station=nearest_station,
                        walk_min=walk_min,
                        rent_yen=rent_yen,
                        management_fee_yen=management_fee_yen,
                        area_m2=area_m2,
                        floor=floor,
                        age_year=room_age_year,
                        structure=room_structure,
                    )
                )
            except Exception as exc:  # noqa: BLE001
                logger.exception("Failed to parse listing row %s-%s: %s", listing_index, row_index, exc)
                continue
    return properties


def _derive_id(listing, row_index: int, url: str, title: str, listing_index: int) -> str:
    raw_id = listing.get("data-bukken-id") or listing.get("data-id")
    if raw_id:
        return f"{raw_id}-{row_index}"
    if url:
        return f"{url}#{row_index}"
    if title:
        return f"{title}-{row_index}"
    return f"listing-{listing_index}-room-{row_index}"


def _title_and_url(anchor) -> tuple[str, str]:
    if anchor is None:
        return "", ""
    if getattr(anchor, "name", "") != "a":
        inner_anchor = anchor.find("a")
        if inner_anchor:
            return inner_anchor.get_text(strip=True), inner_anchor.get("href", "")
        return anchor.get_text(strip=True), ""
    return anchor.get_text(strip=True), anchor.get("href", "")


def _parse_walk_minutes(text: str) -> int:
    match = re.search(r"歩\s*(\d+)\s*分", text)
    if not match:
        return 0
    return int(match.group(1))


def _text(element) -> str:
    if element is None:
        return ""
    return element.get_text(" ", strip=True)


def _href(element) -> str:
    if element is None:
        return ""
    return element.get("href", "")


def _nonempty_texts(elements: Iterable) -> List[str]:
    return [text for text in (_text(el) for el in elements) if text]
