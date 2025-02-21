import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app, TelcoCustomerInput, predict_customer_churn
import pandas as pd

client = TestClient(app)

def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to the Telco Customer Churn Prediction API. Use /docs to access the Swagger UI.'}
    
def test_predict_churn(monkeypatch):
    data = TelcoCustomerInput(
        customerID="7590-VHVEG",
        gender="Female",
        SeniorCitizen=0,
        Partner="Yes",
        Dependents="No",
        tenure=1,
        PhoneService="No",
        MultipleLines="No phone service",
        InternetService="DSL",
        OnlineSecurity="No",
        OnlineBackup="Yes",
        DeviceProtection="No",
        TechSupport="No",
        StreamingTV="No",
        StreamingMovies="No",
        Contract="Month-to-month",
        PaperlessBilling="Yes",
        PaymentMethod="Electronic check",
        MonthlyCharges=29.85,
        TotalCharges="29.85",
        Churn="No"
    )

    monkeypatch.setattr("app.main.predict_model", lambda model, data: pd.DataFrame({"prediction_label": [0], "prediction_score": [0.5]}))
    
    response = predict_customer_churn(object(), data)
    assert response["prediction"] == 0
    assert response["score"] == 0.5