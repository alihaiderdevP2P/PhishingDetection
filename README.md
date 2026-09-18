# Machine Learning-Based Intelligent Phishing and Scam Detection System

Academic prototype: extract **URL + NLP** features from email, SMS, website URLs, and chat text; compare six classifiers; explain the selected model; serve a **Safe / Suspicious / Phishing** interface. This is **not** a production security product.

## What you get

- Deterministic labelled corpus (`python -m src.dataset`)
- URL lexical features and message cue-word / obfuscation features
- Leak-safe scaling fitted on the training split
- Logistic Regression, Naive Bayes, Random Forest, SVM, KNN, XGBoost
- Stratified 80/20 split, 5-fold CV on train, scores on test
- Flask UI with four input modes

## Setup

```bash
cd PhishingDetection
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Build data and train

```bash
python -m src.dataset
python -m src.train
```

or `python run_train.py`. This writes:

- `models/best_model.joblib` — winning pipeline
- `reports/model_comparison.json` — scores used by the web app
- `reports/figures/` — EDA and confusion matrices

## Run the web app

```bash
python run_app.py
```

Open [http://127.0.0.1:5001](http://127.0.0.1:5001). Use the sample buttons to try Safe, Suspicious, and Phishing examples.

## Project layout

```
data/phishing.csv       generated labelled rows (see data/DATASET.md)
src/                    features, training, evaluation, SHAP, prediction
app/                    Flask UI
models/                 saved pipelines (after training)
reports/                metrics and figures
docs/PROPOSAL.md        FYP proposal text
```

## Scope

Included: prototype dataset, URL+NLP features, model comparison, explainability, web demo.

Not included: live mail-server hooks, guaranteed blocking of real attacks, legal enforcement.
