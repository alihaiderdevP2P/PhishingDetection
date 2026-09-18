# Dataset notes

## Task

Three-class classification of a **channel** (email, SMS, chat, URL) plus **message text** and an optional **URL**.

| Label | Name | Meaning in this prototype |
|---|---|---|
| 0 | Safe | Ordinary login pages, transactional mail, or everyday chat with no scam cues |
| 1 | Suspicious | Mixed or weak signals (odd shortening, urgency without a clear payload, unusual host) |
| 2 | Phishing | Strong impersonation, credential/payment harvest, or high-risk URL structure |

## Source

`data/phishing.csv` is built by `python -m src.dataset` (deterministic seed). It is an **academic stand-in** so the pipeline runs without downloading restricted phishing feeds.

The same columns work if you later replace the file with public corpora (URL feature sets, SMS spam collections, or phishing-email archives) after mapping labels to `{0,1,2}`.

## Columns

| Column | Description |
|---|---|
| `channel` | `email`, `sms`, `chat`, or `url` |
| `text` | Message body (may be empty for URL-only rows) |
| `url` | Linked or standalone URL (may be empty) |
| `label` | 0 / 1 / 2 as above |
| `label_name` | Safe / Suspicious / Phishing |

## Leakage rule

Class names and generation templates are **not** passed into the model. Training uses only features computed from `text` and `url` (see `src/features.py`).
