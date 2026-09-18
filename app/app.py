"""Flask prototype for phishing / scam classification (academic demo)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import MODEL_FILES  # noqa: E402
from src.predict import predict_input  # noqa: E402

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)
app.secret_key = "phishguard-fyp-prototype"

SAMPLES = {
    "safe": {
        "channel": "email",
        "text": "Hi team, the weekly status deck is in the shared drive. See you Thursday.",
        "url": "https://github.com/login",
    },
    "suspicious": {
        "channel": "sms",
        "text": "Your mailbox is almost full. Clean it using the short link we sent.",
        "url": "http://bit.ly/acc-3101",
    },
    "phishing": {
        "channel": "email",
        "text": "URGENT: Your PayPal account will be SUSPENDED. Verify now. Enter password and CVV.",
        "url": "http://paypa1-secure-login.tk/update?session=4001",
    },
}


def _metrics_payload() -> dict | None:
    if not MODEL_FILES["metrics"].exists():
        return None
    return json.loads(MODEL_FILES["metrics"].read_text(encoding="utf-8"))


@app.context_processor
def inject_globals():
    return {"models_ready": MODEL_FILES["best_model"].exists()}


@app.route("/")
def index():
    return render_template("index.html", metrics=_metrics_payload(), samples=SAMPLES)


@app.route("/predict", methods=["POST"])
def predict():
    if not MODEL_FILES["best_model"].exists():
        flash("Train the models first: python run_train.py")
        return redirect(url_for("index"))
    channel = (request.form.get("channel") or "message").strip().lower()
    text = (request.form.get("text") or "").strip()
    url = (request.form.get("url") or "").strip()
    if not text and not url:
        flash("Enter a message, a URL, or both.")
        return redirect(url_for("index"))
    try:
        result = predict_input(text, url, channel=channel)
    except Exception as exc:
        flash(str(exc))
        return redirect(url_for("index"))
    return render_template(
        "result.html",
        result=result,
        text=text,
        url=url,
        metrics=_metrics_payload(),
    )


@app.route("/models")
def models():
    payload = _metrics_payload()
    if payload is None:
        flash("No evaluation report found. Run python run_train.py first.")
        return redirect(url_for("index"))
    return render_template("models.html", metrics=payload)


@app.route("/about")
def about():
    return render_template("about.html", metrics=_metrics_payload())


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
