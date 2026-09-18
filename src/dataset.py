"""Deterministic labelled corpus for the phishing prototype."""

from __future__ import annotations

import itertools
import random
from pathlib import Path

import pandas as pd

from src.config import DATA_PATH, RANDOM_STATE, PROJECT_ROOT

SAFE_EMAILS = [
    "Hi team, the weekly status deck is in the shared drive. See you Thursday.",
    "Your package from the bookstore was delivered today. Track it in your orders page.",
    "Reminder: office closed on Monday for the public holiday. Reply if you need anything.",
    "Thanks for your payment. Receipt {n} is attached for your records.",
    "Meeting notes from today are in the usual folder. No action needed tonight.",
    "Your subscription renewal for the news app succeeded. Next bill is next month.",
    "Hi, can you review the draft before 5pm? Link is on the intranet.",
    "Welcome to the course portal. Your instructor posted the first assignment.",
    "Please verify your class attendance on the university LMS before Friday.",
    "IT: password reset completed in the official portal. If this was not you, visit the help desk.",
]

SAFE_SMS = [
    "Your OTP for the bank app is {n}. Do not share it. It expires in 5 minutes.",
    "Ride arriving in 4 min. Plate {n}K. Open the app for the live map.",
    "Pharmacy: your prescription is ready for pickup until 8pm.",
    "Class cancelled tomorrow. New slot posted on the LMS.",
    "Mom: I am at the gate. Come down when you can.",
    "Electricity bill auto-pay went through. Amount is the usual monthly charge.",
]

SAFE_CHAT = [
    "Are we still on for lunch at 1?",
    "Sending the notes in a minute.",
    "Got it, thanks.",
    "Can you share the GitHub repo link when you have a second?",
    "The wifi password is on the fridge as usual.",
]

SAFE_URLS = [
    "https://www.google.com/search?q=python+docs",
    "https://github.com/login",
    "https://www.wikipedia.org/wiki/Phishing",
    "https://support.microsoft.com/en-us/account",
    "https://www.amazon.com/gp/css/order-history",
    "https://accounts.google.com/ServiceLogin",
    "https://www.netflix.com/login",
    "https://www.bbc.com/news",
    "https://stackoverflow.com/questions",
    "https://www.apple.com/shop",
]

SUS_EMAILS = [
    "We noticed a new device. If this was you, ignore this. Otherwise open the portal soon.",
    "Your parcel is delayed. Update delivery preferences using the link we sent separately.",
    "Limited-time offer on cloud storage. Details on our partner page.",
    "IT: please re-authenticate this week. The old token may stop working.",
    "Unusual sign-in from another city. Review activity when you have time.",
]

SUS_SMS = [
    "Delivery attempt failed. Reply YES to reschedule.",
    "You have a pending refund. Call this number when free.",
    "Your mailbox is almost full. Clean it here: http://tinyurl.com/box{n}",
    "Bank: confirm recent purchase of ${n} if you do not recognise it.",
]

SUS_CHAT = [
    "Hey can you check this file for me? Looks official but I am not sure.",
    "Someone asked me to install a remote app. Does that sound right?",
    "Got a short link from a coworker. Opening later maybe.",
]

SUS_URLS = [
    "http://bit.ly/acc-{n}",
    "https://secure-login-update.xyz/account",
    "http://tinyurl.com/verify{n}",
    "https://drive-share.top/view?id={n}",
    "http://accounts.google.com.user-check.tk/login",
    "https://appleid.support-help.work/recover",
]

PHISH_EMAILS = [
    "URGENT: Your PayPal account will be SUSPENDED. Verify now: {url} Enter password and CVV.",
    "Apple ID locked after unusual activity. Confirm your password immediately at {url}",
    "You WON $1,000,000 in the international lottery. Pay a processing fee and send SSN to claim.",
    "Microsoft 365: mailbox full. Re-enter credentials here or mail will be deleted: {url}",
    "Tax refund pending. Submit bank account, PIN and OTP on {url} within 24 hours.",
    "DHL: customs fee unpaid. Click {url} and type card number plus CVV to release parcel.",
    "Your bank detected a $9,400 transfer. Stop it by signing in at {url} NOW!",
    "Netflix billing failed. Update card immediately or service ends tonight: {url}",
    "We updated our billing desk. Kindly sign in and confirm your card on {url} when convenient.",
    "Hello customer, your invoice looks unpaid. Use this page to refresh the card on file: {url}",
]

PHISH_SMS = [
    "Your bank account is locked. Verify OTP and password here {url}",
    "Congratulations winner! Claim prize, send gift cards to this chat then open {url}",
    "Pak-Post: pay Rs {n} customs. Enter CVV at {url} or item returned.",
    "WhatsApp: account banned. Restore login {url} immediately.",
]

PHISH_CHAT = [
    "Bro I need you to buy $200 bitcoin gift cards and send codes. Urgent family emergency.",
    "IT support here. Share your email password so we can stop the hacker. Also open {url}",
    "CEO: wire $8,000 to this new vendor today. Do not tell finance. Details {url}",
]

PHISH_URLS = [
    "http://192.168.14.22/paypal/login/verify",
    "http://paypa1-secure-login.tk/update?session={n}",
    "https://appleid.apple.com.recover-account.gq/signin",
    "http://microsoft-office365-login.xyz/secure@account",
    "https://www.bankofamerica.com.secure-auth.ml/online",
    "http://login.amazon.com.customer-verify.click/account",
    "http://bit.ly/pay-now-{n}",
    "https://netflix-billing-update.top/cvv",
]


def _fill(template: str, n: int, url: str = "") -> str:
    return template.replace("{n}", str(n)).replace("{url}", url)


def build_rows(seed: int = RANDOM_STATE) -> pd.DataFrame:
    rng = random.Random(seed)
    rows: list[dict] = []

    def add(channel: str, text: str, url: str, label: int) -> None:
        rows.append(
            {
                "channel": channel,
                "text": text,
                "url": url,
                "label": label,
                "label_name": {0: "Safe", 1: "Suspicious", 2: "Phishing"}[label],
            }
        )

    for i, (text, url) in enumerate(itertools.product(SAFE_EMAILS, SAFE_URLS[:4])):
        add("email", _fill(text, 1000 + i), url if "http" in text.lower() else "", 0)
    for i, msg in enumerate(SAFE_SMS * 4):
        add("sms", _fill(msg, 2000 + i), "", 0)
    for i, msg in enumerate(SAFE_CHAT * 8):
        add("chat", msg, "", 0)
    for i, url in enumerate(SAFE_URLS * 6):
        add("url", "", url, 0)

    for i, text in enumerate(SUS_EMAILS * 6):
        url = _fill(rng.choice(SUS_URLS), 3000 + i)
        add("email", _fill(text, 3000 + i), url, 1)
    for i, msg in enumerate(SUS_SMS * 6):
        add("sms", _fill(msg, 3100 + i), _fill(rng.choice(SUS_URLS), 3100 + i), 1)
    for i, msg in enumerate(SUS_CHAT * 10):
        add("chat", msg, rng.choice(["", _fill(rng.choice(SUS_URLS), 3200 + i)]), 1)
    for i, url in enumerate(SUS_URLS * 8):
        add("url", "", _fill(url, 3300 + i), 1)

    for i, text in enumerate(PHISH_EMAILS * 6):
        url = _fill(rng.choice(PHISH_URLS), 4000 + i)
        add("email", _fill(text, 4000 + i, url), url, 2)
    for i, msg in enumerate(PHISH_SMS * 6):
        url = _fill(rng.choice(PHISH_URLS), 4100 + i)
        add("sms", _fill(msg, 4100 + i, url), url, 2)
    for i, msg in enumerate(PHISH_CHAT * 8):
        url = _fill(rng.choice(PHISH_URLS), 4200 + i)
        add("chat", _fill(msg, 4200 + i, url), url, 2)
    for i, url in enumerate(PHISH_URLS * 8):
        add("url", "", _fill(url, 4300 + i), 2)

    extras = (
        " Kindly review.",
        " Sent from my phone.",
        " Thread {n}.",
        " Thanks.",
        " Please ignore if already done.",
        "",
        "",
    )
    for row in rows:
        if rng.random() < 0.35:
            row["text"] = (row["text"] + rng.choice(extras)).replace("{n}", str(rng.randint(10, 99)))
        if row["label"] == 0 and rng.random() < 0.08:
            row["url"] = rng.choice(SAFE_URLS)
        if row["label"] == 2 and rng.random() < 0.12:
            row["url"] = _fill(rng.choice(SUS_URLS), rng.randint(5000, 5999))
        if row["label"] == 1 and rng.random() < 0.1:
            row["text"] = row["text"] + " Verify only if you recognise this."
    rng.shuffle(rows)
    return pd.DataFrame(rows)


def write_dataset(path: Path | None = None) -> Path:
    path = path or DATA_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    df = build_rows()
    df.to_csv(path, index=False)
    return path


def main() -> None:
    path = write_dataset()
    df = pd.read_csv(path)
    counts = df["label_name"].value_counts().to_dict()
    print(f"Wrote {path.relative_to(PROJECT_ROOT)}  rows={len(df)}  {counts}")


if __name__ == "__main__":
    main()
