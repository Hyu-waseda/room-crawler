from __future__ import annotations

import csv
import logging
import os
from dataclasses import asdict, fields
from pathlib import Path

from bs4 import BeautifulSoup

from scraper.base import fetch_html
from scraper.models import Property
from scraper.suumo import parse_list_page

logging.basicConfig(level=logging.INFO)

SUUMO_SEARCH_URL = "https://suumo.jp/chintai/tokyo/sc_shibuya/?page=1"  # TODO: 条件は適宜変更する
OUTPUT_PATH = Path("data/properties.csv")


def _load_html_soup() -> BeautifulSoup:
    html_file = os.environ.get("SUUMO_HTML_FILE")
    if html_file:
        logging.info("Loading SUUMO HTML from local file: %s", html_file)
        html = Path(html_file).read_text(encoding="utf-8")
        return BeautifulSoup(html, "html.parser")

    logging.info("Fetching SUUMO search page: %s", SUUMO_SEARCH_URL)
    return fetch_html(SUUMO_SEARCH_URL)


def main() -> None:
    try:
        soup = _load_html_soup()
    except Exception as exc:  # noqa: BLE001
        logging.error("Failed to load HTML: %s", exc)
        return

    properties = parse_list_page(soup)
    if not properties:
        logging.warning("No properties parsed. Check selectors or input HTML.")

    field_names = [f.name for f in fields(Property)]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.info("Writing %d properties to %s", len(properties), OUTPUT_PATH)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for item in properties:
            writer.writerow(asdict(item))


if __name__ == "__main__":
    main()
