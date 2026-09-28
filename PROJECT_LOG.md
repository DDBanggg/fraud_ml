# Project Log & Roadmap: Fraud ML Baseline

## Phase 1 — ML Fundamentals & Evaluation Toolkit
Estimated effort: **25–30 hours**

### Module 1 — Classification Fundamentals
- [ ] Binary classification
- [ ] Train / validation / test split
- [ ] Stratified split
- [ ] Time-based split
- [ ] Data leakage
- [ ] Why random splitting can be problematic for temporal transaction data

### Module 2 — Imbalanced Classification Metrics
- [ ] Confusion Matrix
- [ ] Precision
- [ ] Recall
- [ ] F1
- [ ] ROC-AUC
- [ ] PR-AUC
- [ ] Precision-Recall Curve
- [ ] Threshold tuning
- [ ] False Positive / False Negative trade-offs

### Module 3 — Tabular Preprocessing
- [ ] Numerical features
- [ ] Categorical features
- [ ] Missing values
- [ ] `ColumnTransformer`
- [ ] `RobustScaler`
- [ ] `OneHotEncoder`
- [ ] Prevent preprocessing leakage

### Module 4 — Tree-based Models
- [ ] Decision Tree
- [ ] Random Forest
- [ ] Gradient Boosting
- [ ] XGBoost
- [ ] Understand feature importance

### Module 5 — Class Imbalance
- [ ] Class weighting
- [ ] `scale_pos_weight`
- [ ] Random under-sampling
- [ ] SMOTE
- [ ] Understand when synthetic oversampling may be inappropriate for temporal transaction data

---

## Phase 2 — Dataset Acquisition & EDA
- [ ] Define dataset requirements
- [ ] Select a fraud transaction dataset
- [ ] Prefer datasets containing useful transactional/entity/time information
- [ ] Document dataset source and license
- [ ] Store raw dataset under `data/raw/`
- [ ] Do not commit the actual dataset to Git
- [ ] Inspect schema
- [ ] Check target distribution
- [ ] Check missing values
- [ ] Check duplicate records
- [ ] Check categorical columns
- [ ] Check numerical distributions
- [ ] Check timestamp information
- [ ] Check temporal continuity
- [ ] Identify possible data leakage

---

## Phase 3 — Preprocessing & Feature Engineering
- [ ] Define feature types
- [ ] Implement preprocessing pipeline
- [ ] Implement `ColumnTransformer`
- [ ] Handle numerical features
- [ ] Handle categorical features
- [ ] Handle missing values where necessary
- [ ] Implement train/test split
- [ ] Implement time-based split when appropriate
- [ ] Avoid preprocessing leakage
- [ ] Create meaningful transaction-level features
- [ ] Document every engineered feature

---

## Phase 4 — Model Benchmarking & Tuning

### Baseline
- [ ] Logistic Regression
- [ ] Establish baseline metrics

### Tree Models
- [ ] Random Forest
- [ ] XGBoost

### Evaluation
- [ ] Precision
- [ ] Recall
- [ ] F1
- [ ] PR-AUC
- [ ] ROC-AUC
- [ ] Confusion Matrix
- [ ] Precision-Recall Curve

### Analysis
- [ ] Compare model performance
- [ ] Compare class-weighting strategies
- [ ] Investigate threshold selection
- [ ] Analyze false positives
- [ ] Analyze false negatives
- [ ] Check possible overfitting
- [ ] Document limitations

---

## Phase 5 — Final Report & Future Work
- [ ] Finalize methodology
- [ ] Compile experiment tables
- [ ] Generate PR curves
- [ ] Generate relevant figures
- [ ] Document model comparison
- [ ] Discuss limitations
- [ ] Discuss class imbalance
- [ ] Discuss temporal leakage
- [ ] Write conclusions
- [ ] Define future streaming architecture

### Future Direction
Potential future extension:

```text
Batch Fraud ML
      ↓
Streaming Data
      ↓
Kafka / Confluent
      ↓
Flink
      ↓
Real-time Feature Engineering
      ↓
Online ML Inference
      ↓
Fraud Detection / Alert
```
