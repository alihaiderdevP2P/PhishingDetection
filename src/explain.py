"""Global feature influence for the selected phishing model."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import FIGURES_DIR


def _tree_importances(pipeline, feature_names: list[str]) -> list[dict]:
    model = pipeline.named_steps["model"]
    if not hasattr(model, "feature_importances_"):
        return []
    values = np.asarray(model.feature_importances_, dtype=float)
    order = np.argsort(values)[::-1]
    return [
        {"feature": feature_names[i], "importance": float(values[i])}
        for i in order
    ]


def _linear_importances(pipeline, feature_names: list[str]) -> list[dict]:
    model = pipeline.named_steps["model"]
    if not hasattr(model, "coef_"):
        return []
    coef = np.mean(np.abs(np.asarray(model.coef_)), axis=0)
    order = np.argsort(coef)[::-1]
    return [
        {"feature": feature_names[i], "importance": float(coef[i])}
        for i in order
    ]


def explain_best_model(pipeline, x_train, feature_names: list[str]) -> list[dict]:
    items = _tree_importances(pipeline, feature_names) or _linear_importances(pipeline, feature_names)
    if not items:
        model = pipeline.named_steps["model"]
        if hasattr(model, "feature_importances_") or hasattr(model, "coef_"):
            items = []
        else:
            # Permutation-free fallback: variance of scaled columns as a weak stand-in.
            scaled = pipeline.named_steps["prep"].transform(x_train)
            var = np.var(scaled, axis=0)
            order = np.argsort(var)[::-1]
            items = [
                {"feature": feature_names[i], "importance": float(var[i])}
                for i in order
            ]

    try:
        import shap

        model = pipeline.named_steps["model"]
        transformed = pipeline.named_steps["prep"].transform(x_train)
        sample = transformed[: min(200, len(transformed))]
        if hasattr(model, "feature_importances_"):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(sample)
            if isinstance(shap_values, list):
                mag = np.mean([np.abs(sv).mean(axis=0) for sv in shap_values], axis=0)
            else:
                mag = np.abs(shap_values).mean(axis=0)
                if mag.ndim > 1:
                    mag = mag.mean(axis=-1)
            order = np.argsort(mag)[::-1]
            items = [
                {"feature": feature_names[i], "importance": float(mag[i])}
                for i in order
            ]
    except Exception:
        pass

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    top = items[:12]
    fig, ax = plt.subplots(figsize=(8, 5))
    names = [r["feature"] for r in reversed(top)]
    vals = [r["importance"] for r in reversed(top)]
    ax.barh(names, vals, color="#1d6a7a")
    ax.set_title("Global feature influence (selected model)")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "global_influence.png", dpi=140)
    plt.close(fig)
    pd.DataFrame(items).to_csv(FIGURES_DIR.parent / "feature_importance.csv", index=False)
    return items
