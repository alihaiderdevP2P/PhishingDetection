"""Score a single email / SMS / URL / message."""

from __future__ import annotations

import joblib
import numpy as np
import pandas as pd

from src.config import LABEL_NAMES, MODEL_FILES
from src.features import FEATURE_COLUMNS, featurize_record


def _local_contributions(pipeline, x_row: pd.DataFrame) -> list[dict]:
    model = pipeline.named_steps["model"]
    transformed = pipeline.named_steps["prep"].transform(x_row)
    names = FEATURE_COLUMNS
    contribs: list[tuple[str, float]] = []
    if hasattr(model, "feature_importances_"):
        values = np.asarray(model.feature_importances_) * np.abs(transformed[0])
        contribs = list(zip(names, values.tolist()))
    elif hasattr(model, "coef_"):
        # Mean absolute class coefficient times scaled value.
        coef = np.mean(np.abs(np.asarray(model.coef_)), axis=0)
        values = coef * transformed[0]
        contribs = list(zip(names, values.tolist()))
    else:
        contribs = list(zip(names, np.abs(transformed[0]).tolist()))

    contribs.sort(key=lambda item: abs(item[1]), reverse=True)
    out = []
    for name, value in contribs[:8]:
        out.append(
            {
                "label": name.replace("_", " "),
                "contribution": float(value),
                "direction": "raises risk" if value > 0 else "lowers risk",
            }
        )
    return out


def predict_input(text: str, url: str, channel: str = "message") -> dict:
    if not MODEL_FILES["best_model"].exists():
        raise FileNotFoundError("Train the models first: python -m src.train")
    pipeline = joblib.load(MODEL_FILES["best_model"])
    metadata = joblib.load(MODEL_FILES["metadata"]) if MODEL_FILES["metadata"].exists() else {}
    feats = featurize_record(text or "", url or "")
    x_row = pd.DataFrame([feats], columns=FEATURE_COLUMNS)
    pred = int(pipeline.predict(x_row)[0])
    try:
        proba = pipeline.predict_proba(x_row)[0]
        classes = list(pipeline.classes_)
        dist = {LABEL_NAMES[int(c)]: float(proba[i]) for i, c in enumerate(classes)}
    except Exception:
        dist = {name: (1.0 if name == LABEL_NAMES[pred] else 0.0) for name in LABEL_NAMES.values()}
    return {
        "channel": channel,
        "label": pred,
        "verdict": LABEL_NAMES[pred],
        "probabilities": dist,
        "phishing_probability": float(dist.get("Phishing", 0.0)),
        "model_name": metadata.get("best_model", "saved pipeline"),
        "contributions": _local_contributions(pipeline, x_row),
        "features": feats,
    }
