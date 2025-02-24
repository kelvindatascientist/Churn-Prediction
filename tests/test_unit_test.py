import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app, TelcoCustomerInput, predict_customer_churn
import pandas as pd

client = TestClient(app)

def test_home():
    """
    Test the home endpoint of the Telco Customer Churn Prediction API.

    This function sends a GET request to the '/' endpoint and asserts that:
        - The response status code is 200.
        - The response JSON contains the expected welcome message, instructing users to use '/docs' for the Swagger UI.

    These assertions ensure that the API's root endpoint is returning the correct response and guiding users appropriately.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to the Telco Customer Churn Prediction API. Use /docs to access the Swagger UI.'}
    
def test_predict_churn(monkeypatch):
    """
    Test the predict_customer_churn function.
    This test replaces the actual predict_model function with a lambda that returns a predefined pandas DataFrame with a prediction label and score.
    It then calls the predict_customer_churn function and asserts that the output matches the expected prediction (0) and score (0.5).
    Parameters:
        monkeypatch: A pytest monkeypatch fixture used to temporarily override the predict_model function during the test.
    Raises:
        AssertionError: If the prediction or score in the response does not match the expected values.
    """
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