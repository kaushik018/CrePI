# Credit-Score-Predictor
# Credit Score Predictor Backend

A FastAPI-based backend service for predicting credit scores based on user financial data.

## Local Development

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## AWS EC2 Deployment

### Prerequisites
- AWS Account
- EC2 Instance (Ubuntu 22.04 LTS recommended)
- SSH Key Pair

### Deployment Steps

1. **Connect to EC2**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

2. **Update System & Install Dependencies**:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```

3. **Clone & Setup Project**:
```bash
git clone <your-repository-url>
cd credit-score-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Run the Server**:
```bash
# For testing
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# For production (background)
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### Security Configuration

1. Configure EC2 Security Group to allow:
   - Port 22 (SSH)
   - Port 8000 (API)

2. Access the API at:
```
http://your-ec2-public-ip:8000
```

## API Documentation

Once running, visit `/docs` for the Swagger UI documentation:
- Local: `http://localhost:8000/docs`
- Production: `http://your-ec2-public-ip:8000/docs`

## API Endpoints

### POST /predict
Predicts credit score based on user financial data.

**Request Body**:
```json
{
    "income": float,
    "expenses": float,
    "debt": float
}
```

**Response**:
```json
{
    "credit_score": int
}
```

## Validation Rules
- Income must be greater than 0
- Expenses must be 0 or greater
- Debt must be 0 or greater
- Expenses cannot be greater than income 
