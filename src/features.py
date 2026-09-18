"""URL lexical features and NLP cue features for phishing / scam text."""

from __future__ import annotations

import math
import re
from urllib.parse import urlparse

import pandas as pd

from src.config import (
    BRAND_TOKENS,
    CREDENTIAL_CUES,
    MONEY_CUES,
    SUSPICIOUS_TLDS,
    URGENCY_CUES,
    URL_SHORTENERS,
)

IPV4_RE = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
URL_IN_TEXT_RE = re.compile(r"https?://[^\s]+|www\.[^\s]+", re.I)


def _entropy(text: str) -> float:
    if not text:
        return 0.0
    freq: dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    length = len(text)
    return -sum((n / length) * math.log2(n / length) for n in freq.values())


def _count_cues(text: str, cues: tuple[str, ...]) -> int:
    lowered = text.lower()
    return sum(1 for cue in cues if cue in lowered)


def extract_urls_from_text(text: str) -> list[str]:
    return URL_IN_TEXT_RE.findall(text or "")


def url_features(url: str) -> dict[str, float]:
    raw = (url or "").strip()
    if raw and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", raw):
        raw = "http://" + raw
    parsed = urlparse(raw)
    host = (parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""
    full = raw.lower()

    dots = host.count(".")
    tld = host.rsplit(".", 1)[-1] if "." in host else ""
    labels = [p for p in host.split(".") if p]
    brand_in_host = int(any(b in host for b in BRAND_TOKENS))
    brand_in_path = int(any(b in path.lower() for b in BRAND_TOKENS))
    # Brand mentioned in subdomain but TLD is not a well-known brand domain.
    brand_impersonation = int(brand_in_host and tld in SUSPICIOUS_TLDS)

    return {
        "url_present": float(bool((url or "").strip())),
        "url_length": float(len(raw)),
        "host_length": float(len(host)),
        "path_length": float(len(path)),
        "query_length": float(len(query)),
        "num_dots": float(dots),
        "num_hyphens": float(full.count("-")),
        "num_at": float(full.count("@")),
        "num_slashes": float(full.count("/")),
        "num_digits_url": float(sum(ch.isdigit() for ch in raw)),
        "has_https": float(parsed.scheme == "https"),
        "has_ip": float(bool(IPV4_RE.search(host))),
        "has_port": float(parsed.port is not None),
        "num_subdomains": float(max(len(labels) - 2, 0)),
        "suspicious_tld": float(tld in SUSPICIOUS_TLDS),
        "is_shortener": float(host in URL_SHORTENERS or any(host.endswith("." + s) for s in URL_SHORTENERS)),
        "has_at_in_url": float("@" in raw),
        "double_slash_redirect": float(raw.count("//") > 1),
        "url_entropy": _entropy(raw),
        "brand_in_host": float(brand_in_host),
        "brand_in_path": float(brand_in_path),
        "brand_impersonation": float(brand_impersonation),
        "has_login_token": float(any(tok in full for tok in ("login", "signin", "verify", "update", "secure", "account"))),
    }


def text_features(text: str) -> dict[str, float]:
    body = text or ""
    lowered = body.lower()
    letters = [ch for ch in body if ch.isalpha()]
    upper = sum(1 for ch in letters if ch.isupper())
    urls = extract_urls_from_text(body)
    return {
        "text_length": float(len(body)),
        "num_words": float(len(body.split())),
        "num_exclaim": float(body.count("!")),
        "num_question": float(body.count("?")),
        "upper_ratio": float(upper / len(letters)) if letters else 0.0,
        "urgency_cues": float(_count_cues(lowered, URGENCY_CUES)),
        "credential_cues": float(_count_cues(lowered, CREDENTIAL_CUES)),
        "money_cues": float(_count_cues(lowered, MONEY_CUES)),
        "has_url_in_text": float(bool(urls)),
        "num_urls_in_text": float(len(urls)),
        "has_dollar": float("$" in body or "£" in body or "rs" in lowered or "pkr" in lowered),
        "obfuscation": float(bool(re.search(r"[0-9].*[a-z].*[0-9]", lowered)) or "http://" in lowered),
    }


def featurize_record(text: str, url: str) -> dict[str, float]:
    merged_url = (url or "").strip()
    if not merged_url:
        found = extract_urls_from_text(text or "")
        merged_url = found[0] if found else ""
    feats = {}
    feats.update(url_features(merged_url))
    feats.update(text_features(text or ""))
    return feats


FEATURE_COLUMNS = list(featurize_record("sample", "https://example.com").keys())


def featurize_frame(df: pd.DataFrame) -> pd.DataFrame:
    rows = [featurize_record(str(r.get("text", "")), str(r.get("url", ""))) for r in df.to_dict("records")]
    return pd.DataFrame(rows, columns=FEATURE_COLUMNS)
