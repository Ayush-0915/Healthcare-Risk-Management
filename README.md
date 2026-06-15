# 🏥 Healthcare Risk Management Analytics System

An end-to-end **Data Analytics and Machine Learning** project developed using **Python**, **Streamlit**, and **Scikit-learn** to analyze healthcare data, identify patient risk levels, and provide interactive visualizations for data-driven decision-making.

## 📌 Project Overview

The Healthcare Risk Management Analytics System is designed to help healthcare professionals and data analysts explore patient records, monitor risk factors, and gain valuable insights through interactive dashboards and predictive analytics.

The application combines:

- 📊 Data Analytics
- 🤖 Machine Learning
- 📈 Interactive Dashboards
- 🏥 Healthcare Data Visualization

---

# ✨ Features

## 📊 Executive Dashboard

- Total patient overview
- Average age and billing analysis
- Average length of stay
- Risk category distribution
- Monthly admission trends
- Medical condition insights

## 🏥 Patient Explorer

- Search patients by name
- Filter by:
  - Gender
  - Medical Condition
  - Admission Type
  - Risk Category
  - Age
- Sort records dynamically
- Export filtered data as CSV

## 🚨 Risk Analysis

- Risk category distribution
- High-risk patient identification
- Billing analysis by risk level
- Length of stay comparison
- Top medical conditions among high-risk patients
- Executive insights

## 🤖 AI Risk Prediction

- Predict patient risk category using Machine Learning
- Interactive input form
- Real-time prediction
- Confidence score (where supported)
- Risk-based recommendations

## 📈 Advanced Analytics

- Monthly admission trends
- Hospital-wise analysis
- Insurance provider distribution
- Medication usage analysis
- Test result distribution
- Billing comparison across medical conditions

## ℹ️ About

- Project objectives
- Dataset information
- Technologies used
- Risk assessment methodology
- Developer details

---

# 🛠️ Tech Stack

| Category                | Technology                |
| ----------------------- | ------------------------- |
| Programming Language    | Python                    |
| Data Analysis           | Pandas, NumPy             |
| Visualization           | Plotly, Matplotlib        |
| Machine Learning        | Scikit-learn              |
| Dashboard Framework     | Streamlit                 |
| Model Serialization     | Joblib                    |
| Development Environment | Jupyter Notebook, VS Code |

---

# 📂 Project Structure

```text
Healthcare Risk Management Analytics System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── healthcare_dataset.csv
│   ├── cleaned_healthcare_dataset.csv
│   ├── risk_prediction_model.pkl
│   ├── label_encoders.pkl
│   └── target_encoder.pkl
│
├── notebooks/
│   ├── 01_Data_Cleaning.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_Risk_Analysis.ipynb
│   └── 04_Machine_Learning.ipynb
│
└── pages/
    ├── 1_📊_Executive_Dashboard.py
    ├── 2_🏥_Patient_Explorer.py
    ├── 3_🚨_Risk_Analysis.py
    ├── 4_🤖_ML_Predictions.py
    ├── 5_📈_Advanced_Analytics.py
    └── 6_ℹ️_About.py
```

---

# 📊 Dataset

This project uses a synthetic healthcare dataset containing approximately **55,500 patient records**.

The dataset includes:

- Patient demographics
- Age and gender
- Blood type
- Medical conditions
- Admission type
- Admission and discharge dates
- Hospital information
- Insurance provider
- Billing amount
- Medications
- Test results

The dataset is intended for educational, analytical, and machine learning purposes.

---

# 🤖 Machine Learning

The application includes a Random Forest–based prediction module that estimates a patient's risk category using selected healthcare attributes.

### Input Features

- Age
- Gender
- Blood Type
- Medical Condition
- Admission Type
- Medication
- Test Results
- Length of Stay

### Prediction Output

- 🟢 Low Risk
- 🟡 Medium Risk
- 🟠 High Risk
- 🔴 Critical Risk

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/your-username/healthcare-risk-management-analytics.git
```

## Navigate to the project

```bash
cd healthcare-risk-management-analytics
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Streamlit application

```bash
python -m streamlit run app.py
```

---

# 📈 Key Analytics

- Patient demographic analysis
- Risk category segmentation
- Admission trend analysis
- Medical condition frequency analysis
- Hospital performance overview
- Insurance provider distribution
- Medication utilization analysis
- Billing insights
- Length of stay analysis

---

# 🎯 Learning Outcomes

This project demonstrates practical experience in:

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Healthcare Data Analytics
- Interactive Dashboard Development
- Machine Learning Model Development
- Data Visualization
- Predictive Analytics
- Streamlit Application Development

---

# 🔮 Future Enhancements

- User authentication
- PDF report generation
- Advanced predictive models
- Real-time data integration
- Hospital benchmarking dashboard
- Explainable AI (XAI) for predictions
- Cloud deployment
- REST API integration

---

# 👨‍💻 Developer

## Ayush Singh

**Role:** AI/ML Engineer & Data Analyst

Passionate about building intelligent, data-driven solutions using Artificial Intelligence, Machine Learning, and Data Analytics. This project showcases practical skills in data preprocessing, visualization, dashboard development, and predictive modeling.

---

# ⭐ If you found this project useful

If you like this project, consider giving it a ⭐ on GitHub and sharing your feedback!
