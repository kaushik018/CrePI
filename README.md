
# Credit Score Predictor & Improvement Planner

**A full-stack, machine learning-powered web app to predict credit scores and provide actionable improvement recommendations.**

---

## 🚀 Project Overview

Credit Score Predictor is an end-to-end solution that leverages a trained ML model (Python, scikit-learn) and a modern React frontend to:
- Predict a user's credit score from detailed financial data
- Offer personalized, step-by-step improvement suggestions
- Deliver a beautiful, interactive user experience

---

## 🛠️ Tech Stack

- **Frontend:** React, Material UI, Framer Motion
- **Backend:** FastAPI (Python), Pydantic, Uvicorn
- **ML:** scikit-learn, custom feature engineering, model deployment (pickle)
- **DevOps:** Docker-ready, deployable to AWS EC2

---

## 🎯 Key Features

- **ML Credit Score Prediction:**
    - Predicts scores using real financial indicators (income, expenses, debts, payment history, utilization, etc.)
- **Actionable Recommendations:**
    - Personalized, prioritized steps to improve your credit score
- **Modern UI:**
    - Responsive, stepper-based form, real-time feedback, and visual score indicator
- **API-first:**
    - Clean REST API with Swagger docs (`/docs`)
- **Production-Ready:**
    - Input validation, error handling, CORS, and cloud deployment support

---

## 📝 How It Works

1. **User enters financial data** in the React frontend (income, expenses, debts, payment history, etc.)
2. **Frontend calls FastAPI backend** (`/predict` endpoint)
3. **Backend loads ML model** and computes credit score + improvement plan
4. **Results and recommendations** are displayed with visual feedback

---

## 🖥️ Quickstart (Local)

```bash
# 1. Backend setup
cd credit-score-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# API: http://localhost:8000

# 2. Frontend setup
cd ../../Frontend
npm install
npm start
# App: http://localhost:3000
```

---

## ☁️ Deploy to AWS EC2

1. SSH to your EC2 instance
2. Install Python, Node.js, and Git
3. Clone this repo and follow the Quickstart above
4. Open ports 8000 (API) and 3000 (Frontend) in your EC2 security group

---

## 📚 API Example

**POST** `/predict`

Request body (JSON):
```json
{
    "monthly_income": 5000,
    "monthly_expenses": 3000,
    "savings": 10000,
    "on_time_payments": 24,
    "late_payments": 2,
    "missed_payments": 0,
    "credit_limit": 15000,
    "current_balance": 4500,
    "credit_card_debt": 4500,
    "personal_loan": 10000,
    "student_loan": 20000,
    "mortgage": 200000
}
```

Response:
```json
{
    "status": "success",
    "credit_score": 720,
    "improvements": [
        {"timeframe": "Short-term", "action": "Reduce credit card debt", "impact": "High", "steps": ["Pay off $500 this month", "Avoid new charges"]},
        {"timeframe": "Long-term", "action": "Increase on-time payments", "impact": "Medium", "steps": ["Set up auto-pay", "Monitor due dates"]}
    ],
    "message": "Credit score calculated successfully"
}
```

---

## 📈 Why This Project Stands Out (For Recruiters)

- **Full-Stack Ownership:** Designed, built, and deployed both backend and frontend
- **ML Integration:** Real-world ML model in production, not just a demo
- **Modern Best Practices:**
    - API validation, error handling, CORS, modular code
    - Responsive, accessible, and visually appealing UI
- **Cloud-Ready:** Easily deployable to AWS or any cloud
- **Clear Documentation:** Easy for teams to onboard and extend

---

## 📄 License

MIT
