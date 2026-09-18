"""Load data and build a leak-safe scaler for numeric phishing features."""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import DATA_PATH, RANDOM_STATE, TARGET_COLUMN, TEST_SIZE
from src.features import FEATURE_COLUMNS, featurize_frame


def load_dataset(path=None) -> pd.DataFrame:
    path = path or DATA_PATH
    if not path.exists():
        from src.dataset import write_dataset

        write_dataset(path)
    df = pd.read_csv(path)
    df["text"] = df["text"].fillna("").astype(str)
    df["url"] = df["url"].fillna("").astype(str)
    return df


def split_xy(df: pd.DataFrame):
    x = featurize_frame(df)
    y = df[TARGET_COLUMN].astype(int)
    return x[FEATURE_COLUMNS], y


def train_test_split_stratified(df: pd.DataFrame, random_state: int = RANDOM_STATE):
    x, y = split_xy(df)
    return train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=random_state,
    )


def build_preprocessor() -> Pipeline:
    return Pipeline([("scaler", StandardScaler())])
