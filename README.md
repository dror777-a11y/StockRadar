# 📡 StockRadar — Stock Anomaly Detection System

> An end-to-end data pipeline that detects unusual behavior in 30 major tech stocks using statistical anomaly detection, built with Python and visualized in Power BI.

---

## 🔍 What is StockRadar?

StockRadar is a data science project that automatically identifies **abnormal trading activity** across 30 major tech companies over a one-year period. By applying a **Rolling Z-Score** model on both price and volume data, the system flags days where a stock behaved significantly differently from its recent trend — a key signal in financial analysis and algorithmic trading.

The project covers the full data lifecycle:
**Data Collection → Cleaning → Modeling → Enrichment → Visualization**

---

## 💡 Motivation

Anomaly detection is one of the most powerful tools in data-driven decision making. Whether in finance, cybersecurity, or intelligence — the ability to automatically surface unusual patterns from large datasets is a critical skill.

This project was built to demonstrate a complete, production-style data pipeline using real-world financial data, combining engineering, statistical modeling, and business intelligence.

---

## ⚙️ How It Works

### Pipeline Overview

```
Yahoo Finance API
      ↓
data_collection.py     → Pulls 1 year of historical data for 30 stocks
                       → Cleans missing values (forward fill)
                       → Saves to Stocks_data.csv (long format)
      ↓
anomaly_detection.py   → Calculates 30-day Rolling Mean & Std
                       → Computes Z-Score for Close price and Volume
                       → Flags anomalies (|Z-Score| > 2.5)
                       → Enriches data with Type, Direction, Pct Change
                       → Saves to anomaly_results.csv
      ↓
Power BI Dashboard     → 3-page interactive dashboard
                       → Overview, Stock Deep Dive, Deep Analysis
```

### Anomaly Detection Logic

For each stock and each trading day, the system calculates:

```
Z-Score = (Today's Value − 30-day Rolling Mean) / 30-day Rolling Std
```

A day is flagged as an anomaly if:
- `|Z_Score_Close| > 2.5` → Unusual price movement
- `|Z_Score_Volume| > 2.5` → Unusual trading volume
- Or **both** simultaneously → Strongest signal

> A Rolling Window is used instead of a historical average to ensure the model adapts to the current market regime and avoids false positives from outdated baselines.

---

## 📊 Dashboard

The Power BI dashboard consists of 3 pages:

| Page | Description |
|------|-------------|
| **Overview** | KPI cards (441 anomalies, 30 stocks), anomalies by ticker, anomalies over time |
| **Stock Deep Dive** | Line chart of closing price, anomaly table filtered by stock and date |
| **Deep Analysis** | Anomaly type breakdown, direction distribution, Z-Score scatter plot, top anomalies table |

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| `Python 3.13` | Core programming language |
| `pandas` | Data manipulation and transformation |
| `numpy` | Numerical computations (Z-Score, np.select) |
| `yfinance` | Real-time financial data from Yahoo Finance |
| `Power BI` | Interactive dashboard and visualization |
| `Git / GitHub` | Version control |

---

## 📁 Project Structure

```
StockRadar/
├── src/
│   ├── data_collection.py      # Stage 1: Pull, clean and save stock data
│   └── anomaly_detection.py    # Stage 2: Model, enrich and export anomalies
├── data/
│   ├── Stocks_data.csv         # Raw cleaned data (30 stocks × ~250 days)
│   └── anomaly_results.csv     # Final enriched output with anomaly flags
├── Stocks-Anomalies DASHBOARD.pbix   # Power BI dashboard file
└── README.md
```

---

## 🔑 Key Findings

- **441 anomalies** were detected across 30 stocks over one year
- **CRM (Salesforce)** had the highest anomaly count, suggesting high volatility relative to its own trend
- **44% of anomalies** were driven by Close price movement, **42%** by Volume spikes, and **13%** by both simultaneously — indicating that price and volume anomalies are mostly independent signals
- Anomaly clusters were observed around **major market events** (April 2025, January 2026), consistent with broad market volatility periods
- The strongest single anomaly recorded was **AMD on October 6, 2025** with a combined Z-Score of 4.65 (Close) and 5.02 (Volume)

---

## 🚀 How to Run

**1. Clone the repository:**
```bash
git clone https://github.com/dror777-a11y/StockRadar.git
cd StockRadar
```

**2. Install dependencies:**
```bash
pip install yfinance pandas numpy
```

**3. Run the data collection script:**
```bash
python src/data_collection.py
```

**4. Run the anomaly detection script:**
```bash
python src/anomaly_detection.py
```

**5. Open the dashboard:**
Open `Stocks-Anomalies DASHBOARD.pbix` in Power BI Desktop and click **Refresh** to load the latest data.

---

## 📌 Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Data format | Long format (one row per stock per day) | Compatible with Power BI slicers and filters |
| Missing values | Forward fill (`ffill`) on wide format | Preserves same-stock continuity |
| Anomaly threshold | Z-Score > 2.5 | Balances sensitivity and specificity |
| Rolling window | 30 days | Adapts to current market regime |
| Z-Score on Volume | Primary signal | Volume spikes precede price moves |
| Architecture | Two separate scripts | Decouples data refresh from analysis |

---

*Built by Dror Barel | Industrial Engineering & Management Student*
