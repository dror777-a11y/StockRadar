# 📋 StockRadar — Design Decisions & Reasoning

This document explains every key decision made throughout the project, including the reasoning behind each choice. It serves as a technical reference for understanding the project's architecture and methodology.

---

## 1. Data Collection

### Why 30 large tech companies?
I chose 30 well-known tech companies (AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, etc.) because they are widely recognized, heavily traded, and have reliable data availability. Using familiar companies also makes the results easier to interpret and present.

### Why one year of historical data?
One year provides enough history to calculate meaningful rolling statistics (30-day windows) while keeping the dataset manageable and relevant to current market conditions.

### Why Long Format instead of Wide Format?
Each row in the dataset represents one stock on one trading day. This is the standard format in data science and is directly compatible with Power BI slicers and filters. Wide format would make it significantly harder to filter by stock or date in the dashboard.

### Why separate data collection from anomaly detection (two scripts)?
Downloading data for 30 stocks on every run is slow and unnecessary. By separating the two scripts, I can refresh the data once per day by running `data_collection.py`, and then run `anomaly_detection.py` as many times as needed without re-downloading anything. This mirrors how real production data pipelines are architected.

---

## 2. Data Cleaning

### Why Forward Fill (`ffill`) for missing values?
The stock market is closed on weekends and holidays, which creates gaps in the data. Forward fill replaces missing values with the last known value of the **same stock**. This is the most logical approach for financial time series because the last traded price remains the most relevant reference point until the market reopens.

### Why apply `ffill` on the Wide Format before stacking?
If we applied forward fill after converting to Long Format, the "previous row" for a missing value would belong to a **different stock** (sorted alphabetically), not the same stock. This would produce incorrect fill values. Applying it on Wide Format ensures each missing value is filled with the previous value of the same stock.

---

## 3. Anomaly Detection Model

### Why Rolling Z-Score instead of a global Z-Score?
A global Z-Score compares each data point to the entire historical average. This is problematic because a stock that grew from low to high volume over the year would constantly appear anomalous in early periods and normal in later periods — even if nothing unusual happened. A Rolling Z-Score uses only the last 30 days as the reference window, making it adaptive to the current market regime.

### Why a 30-day rolling window?
30 days (~one trading month) is a standard window in financial analysis. It is long enough to establish a stable baseline but short enough to reflect current market conditions. A shorter window would be too sensitive to noise; a longer window would be too slow to adapt.

### Why Z-Score threshold of 2.5?
In a normal distribution, a Z-Score above 2.5 means the value is in the top ~0.6% of observations. This is strict enough to filter out random noise while still capturing meaningful anomalies. A threshold of 2.0 produced too many false positives; 3.0 missed genuinely interesting events.

### Why calculate Z-Score on both Volume AND Close price?
- **Volume** is the early warning signal — unusual trading activity often precedes price movement, as informed traders act before news becomes public.
- **Close price** is the confirmation signal — it shows the actual market impact of the event.
- Using both together produces stronger, more reliable anomaly signals. A day flagged by both simultaneously is a particularly strong signal.

### Why calculate Direction only on Close price, not Volume?
Volume is always a positive number and a spike in volume is always "unusual" regardless of direction. Direction (Up/Down) only makes logical sense for price movement — it tells us whether the anomaly represented a rally or a selloff.

---

## 4. Data Enrichment

### Why add `Anomaly_Type` (Close / Volume / Both)?
Knowing *what* caused an anomaly is as important as knowing *that* it occurred. A volume-only anomaly suggests unusual trading activity without a corresponding price move. A price-only anomaly suggests a sharp move on normal volume. Both together is the strongest possible signal.

### Why add `Close_Pct_Change` and `Volume_Pct_Change`?
Z-Scores are statistical measures that are not intuitive to non-technical audiences. Percentage deviation from the mean (e.g., "volume was 85% above the 30-day average") is immediately understandable to anyone and makes the dashboard more accessible.

### Why replace NaN values with 0 before export?
The first 29 rows of each stock have no rolling statistics (not enough history yet). These NaN values cause type conversion issues in Power BI. Replacing them with 0 allows Power BI to correctly identify the columns as numeric while clearly distinguishing "no data yet" rows from actual anomalies (which are filtered by `Is_Anomaly = True`).

---

## 5. Power BI Dashboard

### Why three separate pages?
Each page answers a different question:
- **Overview**: "What is the overall picture across all stocks?"
- **Stock Deep Dive**: "What happened to this specific stock over time?"
- **Deep Analysis**: "What patterns exist across all anomalies?"

Separating them prevents information overload and guides the viewer through a logical narrative.

### Why disconnect the "Anomalies by Date" chart from the Ticker slicer?
This chart shows the overall market-wide anomaly trend over time. Filtering it by a single stock removes the broader context and makes it less meaningful. It is intentionally kept at the market level so viewers can see whether anomaly clusters coincide with broad market events.

### Why use Average instead of Sum for Close price in charts?
Each date has exactly one Close value per stock. Power BI defaults to Sum, which would add prices across all selected stocks — a meaningless number. Average correctly returns the single price for the selected stock when a Ticker slicer is applied.

---

## 6. Project Architecture Summary

| Decision | Choice | Alternative Considered | Reason for Choice |
|----------|--------|----------------------|-------------------|
| Data format | Long format | Wide format | Power BI compatibility |
| Missing values | Forward fill | Drop rows | Preserves data continuity |
| Fill timing | Before stack (wide) | After stack (long) | Ensures same-stock fill |
| Anomaly model | Rolling Z-Score | Global Z-Score | Adapts to market regime |
| Rolling window | 30 days | 20 or 60 days | Standard financial window |
| Anomaly threshold | 2.5 | 2.0 or 3.0 | Balance sensitivity/accuracy |
| Direction signal | Close only | Close + Volume | Volume has no meaningful direction |
| Architecture | Two scripts | One combined script | Decouples refresh from analysis |

---

*StockRadar — Built by Dror Barel*
