from fastapi import FastAPI
from pycaret.classification import load_model, predict_model
from pydantic import BaseModel, Field #
from typing import Optional
import pandas as pd
import pdb

class TelcoCustomerInput(BaseModel):
    customerID: str = Field(..., example="7590-VHVEG")
    gender: str = Field(..., example="Female")
    SeniorCitizen: int = Field(..., example=0)
    Partner: str = Field(..., example="Yes")
    Dependents: str = Field(..., example="No")
    tenure: int = Field(..., example=1)
    PhoneService: str = Field(..., example="No")
    MultipleLines: str = Field(..., example="No phone service")
    InternetService: str = Field(..., example="DSL")
    OnlineSecurity: str = Field(..., example="No")
    OnlineBackup: str = Field(..., example="Yes")
    DeviceProtection: str = Field(..., example="No")
    TechSupport: str = Field(..., example="No")
    StreamingTV: str = Field(..., example="No")
    StreamingMovies: str = Field(..., example="No")
    Contract: str = Field(..., example="Month-to-month")
    PaperlessBilling: str = Field(..., example="Yes")
    PaymentMethod: str = Field(..., example="Electronic check")
    MonthlyCharges: float = Field(..., example=29.85)
    TotalCharges: str = Field(..., example="29.85")
    Churn: Optional[str] = Field(None, example="No")
    
app = FastAPI(title="Telco Customer Churn Prediction API", version="1.0")

model = load_model('modelos/churn_model')

def predict_customer_churn(model, data: TelcoCustomerInput) -> dict:
    """Predicts customer churn using a trained machine learning model.

    This function takes a trained model and customer data as input, and returns 
    the churn prediction along with its probability score.

    Args:
        model: A trained machine learning model that predicts customer churn
        data (TelcoCustomerInput): Customer data in the form of a TelcoCustomerInput object

    Returns:
        dict: A dictionary containing either:
            - 'prediction': The churn prediction (0 or 1)
            - 'score': The probability score for the prediction
            OR
            - 'error': Error message if required prediction columns are missing

    Raises:
        None explicitly, but may raise exceptions from underlying pandas or model operations
    """
    input_data = pd.DataFrame([data.model_dump(exclude_none=True)])
    prediction = predict_model(model, data=input_data)
    if 'prediction_label' in prediction.columns and 'prediction_score' in prediction.columns:
        return {'prediction': prediction["prediction_label"].iloc[0], 'score': prediction["prediction_score"].iloc[0]}
    else:
        return {'error': 'Required columns are missing in the prediction output'}

@app.post('/predict')
def predict_churn(data: TelcoCustomerInput):
    """
    Predict customer churn based on the provided customer data.

    This endpoint takes customer data as input and returns a churn prediction 
    along with its probability score.

    Args:
        data (TelcoCustomerInput): Customer data in the form of a TelcoCustomerInput object

    Returns:
        dict: A dictionary containing either:
            - 'prediction': The churn prediction (0 or 1)
            - 'score': The probability score for the prediction
            OR
            - 'error': Error message if required prediction columns are missing
    """
    return predict_customer_churn(model, data)

@app.get('/')
def home():
    """
    Root endpoint of the Telco Customer Churn Prediction API.

    This endpoint returns a welcome message and provides information 
    on how to access the Swagger UI for API documentation.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to the Telco Customer Churn Prediction API. Use /docs to access the Swagger UI."}

