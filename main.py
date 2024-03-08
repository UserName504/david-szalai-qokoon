from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import numpy as np
from datetime import datetime

# Variables for final debugging statement:
now = datetime.now()
time_now = now.strftime("%H:%M:%S")#:%f")
date_now = now.strftime("%A, %B %d, %Y")

app = FastAPI()

class AnalysisParams(BaseModel):
    type: str
    start_date: str

def load_data():
    try:
        pnl_data = pd.read_csv("pnl.csv")
        working_capital_data = pd.read_csv("working_capital.csv")
        return pnl_data, working_capital_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV files not found.")

def calculate_cash_flow(pnl_data, working_capital_data):
    try:
        cash_flow = pnl_data["Net_Income"] + pnl_data["Depreciation"]
        cash_flow -= working_capital_data["Inventory"].diff()
        cash_flow += working_capital_data["Accounts_Receivable"].diff()
        cash_flow -= working_capital_data["Accounts_Payable"].diff()
        return cash_flow
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Key Error: {str(e)}")

@app.post("/cash-flow")
async def get_cash_flow(params: AnalysisParams):
    try:
        start_date = datetime.strptime(params.start_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    if params.type not in ["monthly", "quarterly", "yearly"]:
        raise HTTPException(status_code=400, detail="Invalid analysis type. Use 'monthly', 'quarterly', or 'yearly'.")

    try:
        pnl_data, working_capital_data = load_data()
    except HTTPException as e:
        raise e

    try:
        pnl_data["Date"] = pd.to_datetime(pnl_data["Date"])
        working_capital_data["Date"] = pd.to_datetime(working_capital_data["Date"])

        pnl_data = pnl_data[pnl_data["Date"] >= start_date]
        working_capital_data = working_capital_data[working_capital_data["Date"] >= start_date]

        if params.type == "monthly":
            pnl_data = pnl_data.resample("MS", on="Date").sum()
            working_capital_data = working_capital_data.resample("MS", on="Date").last()
        elif params.type == "quarterly":
            pnl_data = pnl_data.resample("QS", on="Date").sum()
            working_capital_data = working_capital_data.resample("QS", on="Date").last()
        else:
            pnl_data = pnl_data.resample("YS", on="Date").sum()
            working_capital_data = working_capital_data.resample("YS", on="Date").last()

        cash_flow = calculate_cash_flow(pnl_data, working_capital_data)

        cash_flow = cash_flow.apply(np.nan_to_num)

        # Convert cash flow values to JSON:
        cash_flow_dict = {str(index): value for index, value in cash_flow.items()}

        return {"cash_flow": cash_flow_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# For debugging purposes:
print(f"All good at {time_now} on {date_now}.")
