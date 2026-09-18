"""Train, compare, and persist phishing classifiers."""

from __future__ import annotations

import json

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from src.config import CV_FOLDS, MODEL_FILES, RANK_KEYS, RANDOM_STATE, REPORTS_DIR
from src.eda import run_eda
from src.evaluate import evaluate_classifier, plot_confusion_matrices
from src.explain import explain_best_model
from src.features import FEATURE_COLUMNS
from src.preprocess import build_preprocessor, load_dataset, train_test_split_stratified


def build_model_zoo(random_state: int = RANDOM_STATE) -> dict:
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=random_state,
        ),
        "Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=8,
            min_samples_leaf=6,
            class_weight="balanced",
            random_state=random_state,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=280,
            max_depth=10,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        ),
        "SVM": SVC(
            kernel="rbf",
            class_weight="balanced",
            random_state=random_state,
        ),
        "KNN": KNeighborsClassifier(n_neighbors=9, weights="distance"),
        "XGBoost": XGBClassifier(
            n_estimators=220,
            max_depth=5,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="multi:softprob",
            eval_metric="mlogloss",
            random_state=random_state,
            n_jobs=-1,
        ),
    }


def _cv_summary(estimator, x_train, y_train) -> dict:
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    scoring = {
        "accuracy": "accuracy",
        "f1_macro": "f1_macro",
        "f1_weighted": "f1_weighted",
    }
    scores = cross_validate(estimator, x_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)
    return {key: float(np.mean(values)) for key, values in scores.items() if key.startswith("test_")}


def _rank_tuple(row: dict) -> tuple:
    return tuple(row[k] for k in RANK_KEYS)


def train_and_compare() -> dict:
    df = load_dataset()
    run_eda(df)
    x_train, x_test, y_train, y_test = train_test_split_stratified(df)

    comparison = []
    fitted = {}
    test_pred = {}

    for name, clf in build_model_zoo().items():
        pipe = Pipeline(
            [
                ("prep", build_preprocessor()),
                ("model", clf),
            ]
        )
        cv_scores = _cv_summary(pipe, x_train, y_train)
        pipe.fit(x_train, y_train)
        metrics = evaluate_classifier(pipe, x_test, y_test)
        row = {
            "model": name,
            **{f"cv_{k.replace('test_', '')}": v for k, v in cv_scores.items()},
            **metrics,
        }
        comparison.append(row)
        fitted[name] = pipe
        test_pred[name] = pipe.predict(x_test)

    comparison.sort(key=_rank_tuple, reverse=True)
    best_name = comparison[0]["model"]
    best_pipe = fitted[best_name]

    plot_confusion_matrices(test_pred, y_test)
    importances = explain_best_model(best_pipe, x_train, FEATURE_COLUMNS)

    MODEL_FILES["best_model"].parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipe, MODEL_FILES["best_model"])
    joblib.dump(fitted, MODEL_FILES["all_models"])
    joblib.dump(FEATURE_COLUMNS, MODEL_FILES["feature_names"])
    metadata = {
        "best_model": best_name,
        "feature_columns": FEATURE_COLUMNS,
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
        "importances": importances,
    }
    joblib.dump(metadata, MODEL_FILES["metadata"])

    payload = {
        "best_model": best_name,
        "ranking_rule": "phishing recall, then macro F1, then accuracy",
        "dataset_rows": int(len(df)),
        "train_size": int(len(x_train)),
        "test_size": int(len(x_test)),
        "class_counts": {str(k): int(v) for k, v in df["label"].value_counts().sort_index().items()},
        "comparison": comparison,
        "importances": importances[:12],
    }
    MODEL_FILES["metrics"].write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Best model: {best_name}")
    for row in comparison:
        print(
            f"{row['model']:22}  phish_rec={row['test_phishing_recall']:.3f}  "
            f"macro_f1={row['test_macro_f1']:.3f}  acc={row['test_accuracy']:.3f}"
        )
    return payload


if __name__ == "__main__":
    train_and_compare()
