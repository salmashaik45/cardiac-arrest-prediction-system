import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("cardiac_arrest.csv")

X = df.drop("Heart Attack Risk", axis=1)
y = df["Heart Attack Risk"]

# -----------------------------
# Train-Test Split (Stratified)
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Scaling
# -----------------------------

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# Models
# -----------------------------

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "SVM": SVC(probability=True, class_weight="balanced"),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

results = {}

# -----------------------------
# Train & Evaluate
# -----------------------------

for name, model in models.items():

    model.fit(X_train_scaled, y_train)

    preds = model.predict(X_test_scaled)
    probs = model.predict_proba(X_test_scaled)[:, 1]

    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds)
    recall = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    roc_auc = roc_auc_score(y_test, probs)
    cm = confusion_matrix(y_test, preds)

    results[name] = {
        "model": model,
        "f1": f1,
        "roc_auc": roc_auc
    }

    print("\n==============================")
    print(f"{name}")
    print("==============================")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")
    print("Confusion Matrix:")
    print(cm)

# -----------------------------
# Select Best Model (Based on F1)
# -----------------------------

best_model_name = max(results, key=lambda x: results[x]["f1"])
best_model = results[best_model_name]["model"]

print("\n==============================")
print(f"Best Model Selected: {best_model_name}")
print("==============================")

# -----------------------------
# Save Model
# -----------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(best_model, "models/best_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("Model and scaler saved successfully.")