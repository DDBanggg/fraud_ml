# Fraud Detection ML Baseline under Severe Class Imbalance

## Project
**Fraud Detection ML Baseline under Severe Class Imbalance**

## Purpose
This is an academic Machine Learning project associated with:
* **IT4930** — Introduction to Data Science
* **IT3190** — Introduction to Machine Learning and Data Mining

The project focuses on understanding, implementing, and benchmarking machine learning approaches for fraudulent transaction detection under severe class imbalance.

It is also intended as groundwork for a future Data Engineering / streaming thesis.

## Current Scope
The current stage is **batch/offline ML only**. Do not implement Kafka, Flink, streaming inference, APIs, databases, or production deployment yet.

```text
Dataset
  ↓
EDA
  ↓
Preprocessing
  ↓
Feature Engineering
  ↓
ML Models
  ↓
Evaluation
```

### Future Extension
A planned future research direction extends this baseline into a distributed streaming pipeline:

```text
Transactions
    ↓
Kafka
    ↓
Flink
    ↓
Streaming Features
    ↓
ML Inference
    ↓
Fraud Decision / Alert
```

## Core Models
* **Logistic Regression** — baseline with balanced class weights
* **Random Forest** — ensemble tree model with balanced class weights
* **XGBoost** — scalable gradient boosting with `scale_pos_weight`

## Evaluation
Because fraud datasets are usually highly imbalanced (often < 1% fraud), accuracy must **not** be used as the primary evaluation metric. The evaluation focuses on:
* **Precision**
* **Recall**
* **F1**
* **PR-AUC** (Area Under the Precision-Recall Curve)
* **ROC-AUC**
* **Confusion Matrix**
* **Precision-Recall Curve**

## Project Structure
```text
fraud_ml/
├── .gitignore
├── requirements.txt
├── README.md
├── PROJECT_LOG.md
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing_pipeline.ipynb
│   └── 03_baseline_and_models.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── features.py
│   ├── models.py
│   └── evaluate.py
└── reports/
    └── figures/
        └── .gitkeep
```

## Setup & Quickstart

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation & modules
python -m compileall src
python -c "from src.data_loader import load_raw_data, split_data; from src.features import build_preprocessor; from src.models import get_models; from src.evaluate import evaluate_predictions, plot_precision_recall_curve; print('Imports OK')"
```
