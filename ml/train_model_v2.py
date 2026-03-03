import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
import joblib

# --------------------------
# Load Dataset
# --------------------------

df = pd.read_csv("heart_disease_uci.csv")

# --------------------------
# Binary Target Conversion
# --------------------------

df["num"] = df["num"].apply(lambda x: 0 if x == 0 else 1)

# --------------------------
# Drop unnecessary columns
# --------------------------

df.drop(columns=["id", "dataset"], inplace=True)

# --------------------------
# Handle Missing Values
# --------------------------

df.fillna(df.median(numeric_only=True), inplace=True)

# --------------------------
# One-hot encode categoricals
# --------------------------

df = pd.get_dummies(df, drop_first=True)

# --------------------------
# Split Features / Target
# --------------------------

X = df.drop("num", axis=1)
y = df["num"]

# --------------------------
# Train/Test Split
# --------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --------------------------
# Scaling
# --------------------------

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# --------------------------
# Train Model
# --------------------------

model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# --------------------------
# Evaluation
# --------------------------

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\nAccuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# --------------------------
# Save Model + Metadata
# --------------------------

joblib.dump(model, "models/best_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(X.columns.tolist(), "models/feature_columns.pkl")

print("\nModel, scaler, and feature columns saved successfully.")