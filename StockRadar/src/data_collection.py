
import yfinance as yf
import pandas as pd
from datetime import date, timedelta



"""
station 1:
in this station we are going to extract all the relevant data from "yahoofinance" about 30 big high-tech companies.
we are going to extract all the closing prices and the volumes for each stock in the last year from today.
List of 30 big high-tech companies we are going to analyze:
AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, NFLX, INTC, PLTR, DUOL, DELL, ORCL, META, CRM, ADBE, AMD, CSCO, QCOM, MRVL, SAP, SONY, SPOT, SHOP, BABA, SNOW, UBER, ABNB, PYPL, ZM, CRWD
"""
data= yf.download(["AAPL", "MSFT", "GOOGL", "AMZN","TSLA", "NVDA", "NFLX", "INTC", "PLTR", "DUOL", "DELL", "ORCL", "META", "CRM", "ADBE", "AMD",
                   "CSCO", "QCOM", "MRVL", "SAP", "SONY", "SPOT", "SHOP", "BABA", "SNOW", "UBER", "ABNB", "PYPL", "ZM", "CRWD"], start=date.today()-timedelta(days=365), end=date.today()) #Creating DF (WIDE format)

#print(data.head())


"""
station 2:
in this station we are going to "clean" the data.
we will take all the missing data from specific dates and fill the with the values from the day before.
then we will have consistency.
"""
data_filled=data.ffill() #filling the null values with the value of the same stock from day before
"""we do the change on the wide format because we want the value of the *same* stock from day before if we would have done it on the long format it wouldn't be the value of the same stock"""

data_long=data_filled.stack().reset_index() #changing the DF to LONG format
relevant_data=data_long[["Date", "Ticker", "Close", "Volume"]] #just the two columns we want (Close, Volume)
print(relevant_data)
"""
station 3:
in this station we are going to save the data as a one big CSV, 
so later we will be able to create an impressive and logical dashboards to conclude some valuable conclusions.
"""
relevant_data.to_csv("../data/Stocks_data.csv", index=False)