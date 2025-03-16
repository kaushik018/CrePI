from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import logging
from typing import Dict, Union, List, Optional
from ml_model.credit_score_calculator import calculate_credit_score

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI with metadata
app = FastAPI(
    title="Credit Score Predictor API",
    description="Predicts credit scores and provides improvement recommendations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FinancialData(BaseModel):
    # Current Financial Status
    monthly_income: float = Field(..., gt=0, description="Monthly income (must be greater than 0)")
    monthly_expenses: float = Field(..., ge=0, description="Monthly expenses (must be 0 or greater)")
    savings: Optional[float] = Field(None, ge=0, description="Total savings amount")
    
    # Credit History
    on_time_payments: Optional[int] = Field(None, ge=0, description="Number of on-time payments")
    late_payments: Optional[int] = Field(None, ge=0, description="Number of late payments")
    missed_payments: Optional[int] = Field(None, ge=0, description="Number of missed payments")
    
    # Credit Utilization
    credit_limit: Optional[float] = Field(None, ge=0, description="Total credit limit across all accounts")
    current_balance: Optional[float] = Field(None, ge=0, description="Current total balance across all accounts")
    
    # Debt Types
    credit_card_debt: Optional[float] = Field(None, ge=0, description="Total credit card debt")
    personal_loan: Optional[float] = Field(None, ge=0, description="Total personal loan amount")
    student_loan: Optional[float] = Field(None, ge=0, description="Total student loan amount")
    mortgage: Optional[float] = Field(None, ge=0, description="Total mortgage amount")

    @validator('monthly_expenses')
    def expenses_must_be_less_than_income(cls, v, values):
        if 'monthly_income' in values and v > values['monthly_income']:
            raise ValueError('Monthly expenses cannot be greater than monthly income')
        return v

    @validator('current_balance')
    def balance_must_be_less_than_limit(cls, v, values):
        if 'credit_limit' in values and values['credit_limit'] is not None and v is not None:
            if v > values['credit_limit']:
                raise ValueError('Current balance cannot be greater than credit limit')
        return v

    class Config:
        schema_extra = {
            "example": {
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
        }

class CreditScoreResponse(BaseModel):
    status: str
    credit_score: int
    improvements: List[Dict[str, Union[str, List[str]]]]
    message: str

@app.get("/", tags=["Health Check"])
async def root() -> Dict[str, str]:
    """
    Root endpoint for API health check and information.
    """
    return {
        "status": "healthy",
        "message": "Credit Score Predictor API v2.0.0 is running",
        "version": "2.0.0",
        "documentation": "/docs"
    }

@app.post("/predict", tags=["Prediction"], response_model=CreditScoreResponse)
async def predict_score(data: FinancialData) -> CreditScoreResponse:
    """
    Predicts a credit score and provides improvement recommendations based on financial data.

    Args:
        data (FinancialData): Comprehensive financial information

    Returns:
        CreditScoreResponse: Predicted credit score and improvement recommendations

    Raises:
        HTTPException: If prediction fails or input validation fails
    """
    try:
        logger.info(f"Received prediction request with data: {data}")
        
        # Convert Pydantic model to dict
        data_dict = data.dict()
        
        # Calculate score and get improvements
        score, improvements = calculate_credit_score(data_dict)
        
        logger.info(f"Calculated credit score: {score}")
        
        return CreditScoreResponse(
            status="success",
            credit_score=score,
            improvements=improvements,
            message="Credit score calculated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error calculating credit score: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Global exception handler for HTTP exceptions
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Global exception handler for all other exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected error occurred"
        }
    )