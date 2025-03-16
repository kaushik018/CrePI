import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os

# Create more realistic sample data
np.random.seed(42)
n_samples = 1000

data = {
    "amount": np.concatenate([
        np.random.normal(3000, 1000, n_samples//2),  # Income amounts
        -np.random.normal(1000, 500, n_samples//2)   # Expense amounts
    ]),
    "transaction_type": np.concatenate([
        np.ones(n_samples//2),    # Income transactions
        np.zeros(n_samples//2)    # Expense transactions
    ]),
    "balance_after_transaction": np.random.normal(5000, 2000, n_samples)
}

# Calculate credit scores based on financial behavior
data["credit_score"] = (
    300 +  # Base score
    (data["balance_after_transaction"] / 10000 * 200) +  # Balance impact
    (data["amount"] / 5000 * 150) +  # Transaction amount impact
    (data["transaction_type"] * 100)  # Transaction type impact
)

# Ensure credit scores are within valid range (300-850)
data["credit_score"] = np.clip(data["credit_score"], 300, 850)

# Create DataFrame
df = pd.DataFrame(data)

# Prepare features and target
X = df.drop("credit_score", axis=1)
y = df["credit_score"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = LinearRegression()
model.fit(X_scaled, y)

# Create model directory if it doesn't exist
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)

# Save model and scaler
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "credit_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

print("Model training completed and saved successfully!")

# Function to predict score
def predict_credit_score(amount, transaction_type, balance):
    """
    Predict credit score based on transaction details.
    
    Args:
        amount (float): Transaction amount (positive for income, negative for expenses)
        transaction_type (int): 1 for income, 0 for expense
        balance (float): Balance after transaction
        
    Returns:
        float: Predicted credit score (300-850)
    """
    try:
        # Load model and scaler
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "credit_model.pkl"), "rb") as f:
            model = pickle.load(f)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaler.pkl"), "rb") as f:
            scaler = pickle.load(f)
        
        # Prepare features
        features = np.array([[amount, transaction_type, balance]])
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Ensure prediction is within valid range
        prediction = np.clip(prediction, 300, 850)
        
        return round(prediction)
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return None

if __name__ == "__main__":
    # Test prediction
    test_prediction = predict_credit_score(3000, 1, 5000)
    print(f"Test prediction for income of $3000 and balance of $5000: {test_prediction}") 