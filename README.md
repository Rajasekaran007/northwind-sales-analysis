# Northwind Sales Analysis

End-to-end analysis of the Northwind sample business database (customers, orders,
products) using SQL, Python, and a dashboard, aimed at answering real business
questions about revenue performance and data quality.

## Business Questions Answered
1. Which products generate the most revenue?
2. Which countries drive the most revenue?
3. How does revenue trend over time, and is there seasonality?
4. *(Dashboard, in progress)* — What does a stakeholder-facing summary look like?

## Key Findings
- **Côte de Blaye** is the top revenue-generating product, contributing nearly
  double the revenue of the next-highest product (Thüringer Rostbratwurst).
- The **USA, France, and Germany** account for a disproportionate share of total
  revenue relative to other countries, suggesting concentrated market strength
  in these three regions.
- **Data quality issue found:** 335 orders (~2% of the 16,282 total) had missing
  country data, traced to 2 customer records with blank `Country` fields.
  Recommended making `Country` a mandatory field at data entry.
- **Seasonal pattern identified:** February consistently generates the lowest
  average monthly revenue (~$2.92M), while December generates the highest
  (~$3.58M) — a gap of roughly 18%, consistent across an 11-year period
  (2012–2023). This suggests reduced order volume following the holiday season.
- SQL and Python (Pandas) analyses were cross-validated and produced identical
  revenue figures, confirming consistency across tools.

## Tools Used
- **SQL (SQLite)** — joins across `Orders`, `Customers`, `Products`, and
  `Order Details`; aggregation and data quality investigation
- **Python (Pandas)** — reproduced SQL findings; added time-series and seasonal
  analysis
- **Power BI / Excel** — *(coming next)*

## Project Structure
```
northwind-sales-analysis/
├── README.md
├── sql/
│   └── queries.sql       # all SQL queries, commented
├── data/
│   └── (exported CSVs)
├── python/                # Pandas analysis (in progress)
└── dashboard/              # Power BI / Excel dashboard (in progress)
```

## Dataset
[Northwind SQLite database](https://github.com/jpwhite3/northwind-SQLite3) — a
classic small-business ERP schema (customers, orders, products, suppliers,
employees, shipping).
