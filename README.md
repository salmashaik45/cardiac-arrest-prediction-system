# Cardiac Arrest Prediction System

An end-to-end IoT-based healthcare system integrating real-time sensor data, Machine Learning models, and a Django web application to predict cardiac risk levels.

---

## 📌 Overview

This project combines IoT, cloud integration, Machine Learning, and a web application to monitor health parameters and predict the risk of cardiac arrest.

The system collects live sensor data (Heart Rate, SpO₂, Body Temperature), integrates it with additional health inputs, and uses a trained ML model to generate risk predictions.

---

## ⚙️ System Architecture

IoT Sensors → ThingSpeak Cloud API → Django Backend → ML Model → Web Interface

---

## 🧠 Machine Learning

- Dataset-based training using multiple classification models
- Feature scaling using MinMaxScaler
- Model serialization using joblib
- Real-time prediction integrated into Django backend

---

## 🌐 Web Application

- Built using Django
- REST-style POST endpoint for prediction
- HTML form interface for user input
- Integration with live sensor data from ThingSpeak

---

## 🛠️ Tech Stack

### Backend
- Python
- Django

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- MinMaxScaler (Feature Scaling)
- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Joblib (Model Serialization)

### IoT
- ESP8266 (NodeMCU)
- MAX30102 (Heart Rate & SpO₂ Sensor)
- DS18B20 (Temperature Sensor)
- ThingSpeak Cloud API

### Frontend
- HTML
- CSS
- JavaScript (Fetch API)

---

## 📂 Project Structure

```
hardware/ → IoT code (ESP8266)
backend/ → Django project
ml/ → Model training and dataset
```

---

## 🚀 How to Run

1. Clone the repository
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run Django server:

```
python manage.py runserver
```

---

## ⚠️ Disclaimer

This project is developed for educational and research purposes only. It is not intended for medical diagnosis or clinical 