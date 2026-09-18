# FYP Proposal

## Proposed title

Machine Learning-Based Intelligent Phishing and Scam Detection System

## Introduction

Phishing and scam messages remain a common way to steal credentials, money, and personal data. Attackers send email, SMS, chat messages, and lookalike website URLs that impersonate banks, delivery firms, and login pages.

Machine learning can combine **URL structure features** with **natural-language cues** from the message body to estimate whether content is safe, suspicious, or phishing. This project builds a leak-safe comparative pipeline and a browser interface that accepts email, SMS, a website URL, or free-text messages.

## Problem statement

People must judge mixed signals — a familiar brand name, an urgent tone, a shortened link, or a slightly misspelled domain — often under time pressure. The problem addressed here is: can a documented ML/NLP prototype classify multi-channel text and URLs into Safe / Suspicious / Phishing on a public-style labelled set, while remaining interpretable enough for an academic demo?

## Aim

To develop and evaluate a machine-learning system that detects phishing and scam content from email, SMS, website URLs, and message text.

## Objectives

1. Assemble a labelled multi-channel dataset (URL + message text) suitable for an academic prototype.
2. Extract URL features (length, host, path, special characters, brand impersonation, HTTPS, IP-in-URL, and related signals).
3. Extract NLP features from message text (urgency, credential requests, money language, obfuscation).
4. Train and compare several classifiers.
5. Evaluate with accuracy, precision, recall, F1, and confusion matrices, with extra weight on catching phishing.
6. Select the best model under a pre-declared ranking rule.
7. Provide feature-level explanations for individual predictions.
8. Deliver a Flask web interface for all four input types.
9. Evaluate the complete prototype.

## Research questions

- Which algorithm performs best for three-class phishing detection on this dataset?
- Which URL and text features most influence the selected model?
- Does combining URL features with NLP improve over URL-only or text-only models?
- How well can the system separate Safe, Suspicious, and Phishing?
- Do explanations make an individual verdict easier to discuss in a viva?

## Dataset

A prototype corpus of labelled email, SMS, chat, and URL examples covering Safe, Suspicious, and Phishing classes. Generation rules and class definitions are in `data/DATASET.md`. The pipeline is written so a later swap to public corpora (e.g. URL datasets, SMS spam, phishing email archives) does not change the training API.

## Algorithms

Logistic Regression (baseline), Naive Bayes, Random Forest, SVM, KNN, XGBoost.

Pipeline: Dataset → Feature extraction (train-only scaling) → Train six models → Cross-validate → Test evaluation → Compare → Explain → Web prototype.

## Methodology

1. **Collection** — labelled multi-channel records (text + optional URL).
2. **Features** — URL lexical/host signals + bag-of-cue NLP counts; scaler fitted on the training split.
3. **EDA** — class balance, URL length, HTTPS rate, cue-word rates.
4. **Development** — stratified 80/20 split; 5-fold stratified CV on train; test set reserved.
5. **Evaluation** — accuracy, macro/weighted F1, per-class recall (phishing recall emphasised), confusion matrix.
6. **Explainability** — global importances and local attributions for the selected model.
7. **Interface** — Flask form for email, SMS, URL, and message text. Wording is **estimated class**, not a guarantee.

## Scope

**In scope:** public-style data, feature engineering, classification, comparison, explainability, web prototype.

**Out of scope:** live email-server integration, browser extension stores, blocking production traffic, legal takedowns, guaranteed protection against zero-day campaigns.

## Expected results

A trained comparative pipeline, a documented winning model *for this dataset and protocol*, influence plots, and a prototype UI that returns Safe / Suspicious / Phishing with supporting features.

## Timeline (indicative)

| Weeks | Activity |
|---|---|
| 1–2 | Topic and proposal |
| 3–4 | Literature review |
| 5 | Dataset and feature design |
| 6–7 | URL + NLP feature extraction |
| 8 | EDA |
| 9–11 | Model development |
| 12 | Comparison |
| 13 | Explainable AI |
| 14–15 | Web application |
| 16 | Testing |
| 17 | Results and discussion |
| 18 | Final report |
| 19 | Presentation and demo |

## Stack

Python, pandas, NumPy, scikit-learn, XGBoost, Matplotlib/Seaborn, SHAP, Flask, HTML/CSS/JavaScript.
