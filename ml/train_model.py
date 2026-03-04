import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix


# ==============================
# Load Dataset
# ==============================

df = pd.read_csv("heart_disease_uci.csv")

# Convert target into binary
df["num"] = df["num"].apply(lambda x: 1 if x > 0 else 0)

# Drop unused columns
df = df.drop(columns=["id", "dataset"])

# Convert boolean to int
df = df.replace({True: 1, False: 0})

# One-hot encode categoricals
df = pd.get_dummies(df, drop_first=True)

# ==============================
# Features / Target
# ==============================

X = df.drop("num", axis=1)
y = df["num"]

# ==============================
# Handle Missing Values
# ==============================

imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

# Save feature names AFTER encoding
feature_columns = X.columns.tolist()

# ==============================
# Train/Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42
)

# ==============================
# Scaling
# ==============================

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==============================
# Model
# ==============================

model = LogisticRegression(max_iter=3000)
model.fit(X_train_scaled, y_train)

# ==============================
# Evaluation
# ==============================

y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

print("\nAccuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ==============================
# Save Everything
# ==============================

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/best_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(imputer, "models/imputer.pkl")
joblib.dump(feature_columns, "models/feature_columns.pkl")

print("\nModel, scaler, imputer, and feature columns saved successfully.")