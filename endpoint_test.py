from fastapi.testclient import TestClient
import pandas as pd
from main import app, calculate_cash_flow

client = TestClient(app)

# Testing accuracy:
def test_calculate_cash_flow():
    pnl_data = pd.DataFrame({
        "Date": ["2022-01-01", "2022-02-01", "2022-03-01"],
        "Net_Income": [1000, 1500, 2000],
        "Depreciation": [100, 150, 200]
    })
    working_capital_data = pd.DataFrame({
        "Date": ["2022-01-01", "2022-02-01", "2022-03-01"],
        "Inventory": [500, 600, 700],
        "Accounts_Receivable": [200, 250, 300],
        "Accounts_Payable": [100, 120, 140]
    })
    
    expected_cash_flow = pd.Series([700.0, 1580.0, 2130.0], name="Cash Flow")
    
    result = calculate_cash_flow(pnl_data, working_capital_data)
    
    pd.testing.assert_series_equal(result, expected_cash_flow)

# Input validation testing:
def test_valid_request():
    response = client.post("/cash-flow", json={
        "type": "monthly",
        "start_date": "2022-01-01"
    })
    assert response.status_code == 200

def test_invalid_analysis_type():
    response = client.post("/cash-flow", json={
        "type": "invalid",
        "start_date": "2022-01-01"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid analysis type. Use 'monthly', 'quarterly', or 'yearly'."}

def test_invalid_date_format():
    response = client.post("/cash-flow", json={
        "type": "monthly",
        "start_date": "2022-01-01T00:00:00"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid start_date format. Use YYYY-MM-DD."}

def test_large_dataset():
    # Generate a dataset for testing purposes:
    dates = pd.date_range(start="2020-01-01", end="2023-12-31", freq="D")
    pnl_data = pd.DataFrame({
        "Date": dates,
        "Net_Income": [1000] * len(dates),
        "Depreciation": [100] * len(dates)
    })
    working_capital_data = pd.DataFrame({
        "Date": dates,
        "Inventory": [500] * len(dates),
        "Accounts_Receivable": [200] * len(dates),
        "Accounts_Payable": [100] * len(dates)
    })
    
    # Save the generated dataset:
    pnl_data.to_csv("pnl_large.csv", index=False)
    working_capital_data.to_csv("working_capital_large.csv", index=False)
    
    response = client.post("/cash-flow", json={
        "type": "monthly",
        "start_date": "2020-01-01"
    })
    assert response.status_code == 200
