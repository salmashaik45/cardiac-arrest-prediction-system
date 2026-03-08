# 🫀 Heart Disease Risk Prediction System with IoT Monitoring

A machine learning–powered web application that predicts the probability of heart disease risk based on clinical inputs. The system integrates a trained ML model with a Django backend API and a web dashboard, while also displaying real-time vital readings from IoT sensors.

## 📌 Project Overview

This project predicts the likelihood of heart disease using a Logistic Regression model trained on the UCI Heart Disease dataset.

Users enter clinical parameters through a web interface. The backend processes these inputs through a trained ML pipeline and returns a risk probability and risk level (Low / Moderate / High).

The system also displays live IoT vital readings collected from sensors connected to an ESP8266 microcontroller and transmitted through the ThingSpeak cloud platform.

## 🚀 Features

- Machine learning–based heart disease risk prediction

- Clean web dashboard for clinical data input

- Django backend API for ML inference

- Real-time IoT vital monitoring

- End-to-end ML pipeline with preprocessing

- Probability-based risk classification

- Modular project structure suitable for deployment

## 🧠 Machine Learning Pipeline

### Dataset

UCI Heart Disease Dataset

### Model

Logistic Regression

### Preprocessing

- Missing value imputation

- One-hot encoding for categorical features

- Feature alignment using saved feature metadata

- Standard scaling

### Evaluation Metrics

| Metric    | Value |
|-----------|-------|
| Accuracy  | ~80%  |
| Precision | ~86%  |
| Recall    | ~79%  |
| F1 Score  | ~0.82 |
| ROC-AUC   | ~0.88 |

## 🏗 System Architecture

```
IoT Sensors (MAX30102, DS18B20)
        │
        ▼
ThingSpeak Cloud Platform
        │
        ▼
Django Backend API
        │
        ▼
Machine Learning Model
        │
        ▼
Prediction Result
        │
        ▼
Web Dashboard UI
```

## 📂 Project Structure

```
cardiac-arrest-prediction-system
│
├── backend
│   ├── manage.py
│   ├── cardiac_predictor
│   └── predictor
│
├── ml
│   ├── train_model.py
│   └── models
│
├── hardware
│   ├── iot-code.ino
│   └── secrets_example.h
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 🖥 Application Interface

### Prediction Form

Users enter clinical health parameters to estimate heart disease risk.

The system returns the probability and classifies the risk.

### Example:

```
Low Risk — 1.66%
Moderate Risk — 44.79%
High Risk — 99.03%
```

## Live IoT Monitoring

The dashboard also displays real-time vital signs:

- Heart Rate

- Oxygen Saturation (SpO₂)

- Body Temperature

These readings are streamed via ThingSpeak.

🧪 Example Predictions
Healthy profile
Age: 28
Sex: Female
Cholesterol: 170
BP: 110
Result → Low Risk (1.66%)
Moderate profile
Age: 52
BP: 140
Cholesterol: 240
Result → Moderate Risk (~45%)
High risk profile
Age: 63
Chest Pain: asymptomatic
Oldpeak: 3.5
Result → High Risk (~99%)
⚙ Installation
Clone repository
git clone https://github.com/yourusername/heart-disease-prediction.git
cd heart-disease-prediction
Create virtual environment
python -m venv venv
Activate environment

Windows

venv\Scripts\Activate
Install dependencies
pip install -r requirements.txt
▶ Running the Application

Navigate to backend:

cd backend

Start Django server:

python manage.py runserver

Open in browser:

http://127.0.0.1:8000
⚠ Disclaimer

This project is intended for educational and research purposes only.
It should not be used as a substitute for professional medical diagnosis.

👩‍💻 Author

Salma
Computer Science & Engineering Student

⭐ If you found this project useful, consider giving it a star.
Small advice for you

For GitHub projects, recruiters love screenshots.

So later you can create a folder:

docs/images/

and add:

form.png
prediction.png
dashboard.png

Then your README will look much more professional.