
"""
in this python file we need to calculate the Z-SCORE for each row in our complete DF ("relevant_data").
we are going to calculate the Z-SCORE for both columns and to see where and if we have some serious deviation.
"""
from email.policy import default
from operator import ifloordiv
import numpy as np
import pandas as pd
"""
station 1:
Load the data from the CSV we created.
"""
data=pd.read_csv("../data/Stocks_data.csv")
#print(data.head())

"""
station 2:
Calculate Rolling Mean and Rolling Std 
for both Volume and Close (window of 30 days, grouped by Ticker)
"""

#calculating the averages:
data["Rolling_Mean_Close"]=data.groupby(["Ticker"])["Close"].rolling(window=30).mean().reset_index(level=0, drop=True)
data["Rolling_Mean_Volume"]=data.groupby(["Ticker"])["Volume"].rolling(window=30).mean().reset_index(level=0, drop=True)

#calculating the std's
data["Rolling_std_Close"]=data.groupby(["Ticker"])["Close"].rolling(window=30).std().reset_index(level=0, drop=True)
data["Rolling_std_Volume"]=data.groupby(["Ticker"])["Volume"].rolling(window=30).std().reset_index(level=0, drop=True)

#testing:
#print(data[data["Ticker"] == "AAPL"].head(35))

"""
station 3:
Calculate the Z-Score for each row
using the formula: (value - rolling_mean) / rolling_std
"""
data["Z_Score_Close"]=(data["Close"]-data["Rolling_Mean_Close"])/data["Rolling_std_Close"]
data["Z_Score_Volume"]=(data["Volume"]-data["Rolling_Mean_Volume"])/data["Rolling_std_Volume"]

#testing:
#print(data[data["Ticker"] == "AAPL"].head(35))

"""
station 4:
Flag anomalies - any row where the absolute Z-Score is above 2.5
"""
data["Is_Anomaly"]=(data["Z_Score_Close"].abs()>2.5) | (data["Z_Score_Volume"].abs()>2.5 )

#testing:
#print(data[data["Ticker"] == "AAPL"].head(35))

#Adding some mew columns:

#Anomaly_Type- determine if the anomaly was caused because of the volume, close or both
choices=["Both", "Volume", "Close"]

conditions=[
    (data["Z_Score_Close"].abs()>2.5) & (data["Z_Score_Volume"].abs()>2.5 ),
    (data["Z_Score_Close"].abs()<=2.5) & (data["Z_Score_Volume"].abs()>2.5 ),
    (data["Z_Score_Close"].abs()>2.5) & (data["Z_Score_Volume"].abs()<=2.5 )
]

data["Anomaly_Type"]=np.select(conditions, choices, default="None")


# Percentage deviation from the mean-Close:


data["Close_Pct_Change"]= ((data["Close"]-data["Rolling_Mean_Close"])/data["Rolling_Mean_Close"]) * 100

# Percentage deviation from the mean-Volume:
data["Volume_Pct_Change"]= ((data["Volume"]-data["Rolling_Mean_Volume"])/data["Rolling_Mean_Volume"]) * 100

#determine the direction of the anomaly-Close:
data["Direction"]= np.where(data["Z_Score_Close"].isna(), "None", np.where((data["Z_Score_Close"]>0), "UP", "DOWN", ))

print(data)

#Converting the fields into decimal numbers instead of text

data["Z_Score_Close"] = data["Z_Score_Close"].round(2)
data["Z_Score_Volume"] = data["Z_Score_Volume"].round(2)
data["Close_Pct_Change"] = data["Close_Pct_Change"].round(2)
data["Volume_Pct_Change"] = data["Volume_Pct_Change"].round(2)

numeric_cols = ["Z_Score_Close", "Z_Score_Volume", "Close_Pct_Change", "Volume_Pct_Change"]
data[numeric_cols] = data[numeric_cols].fillna(0)


data.to_csv("../data/anomaly_results.csv", index=False)
