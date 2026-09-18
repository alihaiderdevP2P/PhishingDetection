"""Test-set metrics for three-class phishing detection."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from src.config import FIGURES_DIR, LABEL_NAMES


def evaluate_classifier(estimator, x_test, y_test) -> dict:
    pred = estimator.predict(x_test)
    labels = [0, 1, 2]
    rec = recall_score(y_test, pred, labels=labels, average=None, zero_division=0)
    prec = precision_score(y_test, pred, labels=labels, average=None, zero_division=0)
    f1 = f1_score(y_test, pred, labels=labels, average=None, zero_division=0)
    return {
        "test_accuracy": float(accuracy_score(y_test, pred)),
        "test_macro_f1": float(f1_score(y_test, pred, average="macro", zero_division=0)),
        "test_weighted_f1": float(f1_score(y_test, pred, average="weighted", zero_division=0)),
        "test_phishing_recall": float(rec[2]),
        "test_phishing_precision": float(prec[2]),
        "per_class_recall": {LABEL_NAMES[i]: float(rec[i]) for i in labels},
        "per_class_precision": {LABEL_NAMES[i]: float(prec[i]) for i in labels},
        "per_class_f1": {LABEL_NAMES[i]: float(f1[i]) for i in labels},
        "report": classification_report(
            y_test, pred, target_names=[LABEL_NAMES[i] for i in labels], zero_division=0
        ),
    }


def plot_confusion_matrices(predictions: dict, y_test, out_dir: Path | None = None) -> None:
    out_dir = out_dir or FIGURES_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    names = list(predictions.keys())
    cols = 3
    rows = int(np.ceil(len(names) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(12, 3.6 * rows))
    axes = np.atleast_1d(axes).ravel()
    labels = [0, 1, 2]
    tick = [LABEL_NAMES[i] for i in labels]
    for ax, name in zip(axes, names):
        cm = confusion_matrix(y_test, predictions[name], labels=labels)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax, xticklabels=tick, yticklabels=tick)
        ax.set_title(name)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
    for ax in axes[len(names) :]:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(out_dir / "confusion_matrices.png", dpi=140)
    plt.close(fig)
