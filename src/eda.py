"""Exploratory plots for the phishing corpus."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import FIGURES_DIR, LABEL_NAMES
from src.features import featurize_frame


def run_eda(df: pd.DataFrame, out_dir: Path | None = None) -> None:
    out_dir = out_dir or FIGURES_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df["label"].map(LABEL_NAMES).value_counts().reindex(["Safe", "Suspicious", "Phishing"])
    counts.plot(kind="bar", color=["#2a9d8f", "#e9c46a", "#e76f51"], ax=ax, rot=0)
    ax.set_ylabel("Rows")
    ax.set_title("Class balance")
    fig.tight_layout()
    fig.savefig(out_dir / "class_balance.png", dpi=140)
    plt.close(fig)

    feats = featurize_frame(df)
    feats["label_name"] = df["label"].map(LABEL_NAMES).values

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=feats, x="label_name", y="url_length", order=["Safe", "Suspicious", "Phishing"], ax=ax)
    ax.set_title("URL length by class")
    fig.tight_layout()
    fig.savefig(out_dir / "url_length_by_class.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=feats,
        x="label_name",
        y="urgency_cues",
        order=["Safe", "Suspicious", "Phishing"],
        ax=ax,
        errorbar="sd",
    )
    ax.set_title("Mean urgency cues by class")
    fig.tight_layout()
    fig.savefig(out_dir / "urgency_cues.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    corr = feats.drop(columns=["label_name"]).corr(numeric_only=True)
    sns.heatmap(corr, ax=ax, cmap="vlag", center=0, xticklabels=False, yticklabels=False)
    ax.set_title("Feature correlation")
    fig.tight_layout()
    fig.savefig(out_dir / "feature_correlation.png", dpi=140)
    plt.close(fig)
