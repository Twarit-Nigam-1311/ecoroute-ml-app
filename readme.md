Markdown

# 🚗 EcoRoute: Full-Stack ML Inference Service

A production-grade Machine Learning microservice that predicts vehicle fuel efficiency (MPG) using **XGBoost**, **FastAPI**, and **Streamlit**.



## 🛠️ Project Structure
* `main.py` - FastAPI Backend & Logging
* `app.py` - Streamlit Dashboard
* `test_api.py` - Pytest Quality Suite
* `production_model.pkl` - Trained Model & Scaler

---

## 🚀 Quick Start (Copy & Paste)

### 1. Install Dependencies
```bash
pip install fastapi[all] uvicorn streamlit joblib scikit-learn xgboost pandas numpy pytest httpx plotly

2. Start the Backend (Terminal 1)
Bash

python -m uvicorn main:app --reload

3. Start the Dashboard (Terminal 2)
Bash

streamlit run app.py

4. Run Automated Tests (Terminal 3)
Bash

pytest test_api.py -v

📊 Features

    Real-time Inference: Sub-100ms response time.

    Data Validation: Pydantic models prevent "garbage-in/garbage-out."

    Audit Logs: All requests saved to api_usage.log.

    Unit Testing: Automated checks for model accuracy and latency.

Author: [Your Name] Project: Full-Stack ML Software Engineering


---

### 💡 Pro-Tip: The "One-Click" Launch
If you want to open both the API and the Dashboard at the same time without typing commands, create a file named **`run_project.bat`** and paste this:

```batch
@echo off
start cmd /k "python -m uvicorn main:app --reload"
timeout /t 5
start cmd /k "streamlit run app.py"
echo 🚀 EcoRoute System is launching...