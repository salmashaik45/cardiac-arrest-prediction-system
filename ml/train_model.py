import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("cardiac_arrest.csv")

X = df.drop("Heart Attack Risk", axis=1)
y = df["Heart Attack Risk"]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

log_model = LogisticRegression()
log_model.fit(X_train, y_train)
log_preds = log_model.predict(X_test)
print(f"Logistic Regression Accuracy: {accuracy_score(y_test, log_preds):.4f}")

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)
print(f"Random Forest Accuracy: {accuracy_score(y_test, rf_preds):.4f}")

svm_model = SVC()
svm_model.fit(X_train, y_train)
svm_preds = svm_model.predict(X_test)
print(f"SVM Accuracy: {accuracy_score(y_test, svm_preds):.4f}")

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)
knn_preds = knn_model.predict(X_test)
print(f"KNN Accuracy: {accuracy_score(y_test, knn_preds):.4f}")

joblib.dump(log_model, "best_model.pkl")
joblib.dump(scaler, "scaler.pkl")

