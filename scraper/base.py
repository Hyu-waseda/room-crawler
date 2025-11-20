from __future__ import annotations

import logging
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
USER_AGENT = "room-scout/0.1 (+https://example.com)"


def fetch_html(url: str, timeout: int = 10) -> BeautifulSoup:
    """Fetch HTML from the given URL and return a BeautifulSoup object."""
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_yen(text: str) -> int:
    """Parse yen amount like '12.3万円', '12.3万', or '80,000円' to integer yen."""
    if text is None:
        return 0

    normalized = text.replace(",", "").replace("円", "").strip()

    man_match = re.match(r"([0-9]+(?:\.[0-9]+)?)\s*万(?:円)?", normalized)
    if man_match:
        value = float(man_match.group(1)) * 10000
        return int(value)

    digits = re.findall(r"\d+", normalized)
    if digits:
        return int("".join(digits))

    return 0


def parse_int(text: Optional[str]) -> int:
    if text is None:
        return 0
    digits = re.findall(r"-?\d+", text)
    if not digits:
        return 0
    return int(digits[0])


def parse_float(text: Optional[str]) -> float:
    if text is None:
        return 0.0
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return 0.0
    return float(match.group(0))
