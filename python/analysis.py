"""
Northwind Sales Analysis — Python (Pandas)
Reproduces the SQL findings and extends the analysis with a monthly
revenue trend.

Requirements: pandas (pip install pandas)
Place northwind.db in the same folder as this script, or update the
path in sqlite3.connect() below.
"""

import sqlite3
import pandas as pd

# ------------------------------------------------------------------
# Setup — load tables from the database
# ------------------------------------------------------------------
conn = sqlite3.connect("northwind.db")

orders = pd.read_sql_query("SELECT * FROM Orders", conn)
order_details = pd.read_sql_query('SELECT * FROM "Order Details"', conn)
products = pd.read_sql_query("SELECT * FROM Products", conn)
customers = pd.read_sql_query("SELECT * FROM Customers", conn)

conn.close()

# ------------------------------------------------------------------
# Task 1 — Merge tables (Pandas equivalent of the SQL joins)
# ------------------------------------------------------------------
merged = (
    order_details
    .merge(orders, on="OrderID")
    .merge(products, on="ProductID")
    .merge(customers, on="CustomerID")
)

# UnitPrice_x = price from Order Details (price at time of sale)
# UnitPrice_y = price from Products (current list price)
# Revenue should be based on the price at time of sale.
merged["Revenue"] = merged["Quantity"] * merged["UnitPrice_x"]

# ------------------------------------------------------------------
# Task 2 — Reproduce SQL findings: top products and revenue by country
# ------------------------------------------------------------------
top_products = (
    merged.groupby("ProductName")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

revenue_by_country = (
    merged.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("=== Top 10 Products by Revenue ===")
print(top_products)
print()

print("=== Revenue by Country ===")
print(revenue_by_country)
print()

# ------------------------------------------------------------------
# Task 3 — New analysis: monthly revenue trend
# ------------------------------------------------------------------
merged["OrderDate"] = pd.to_datetime(merged["OrderDate"], format="mixed")
merged["YearMonth"] = merged["OrderDate"].dt.to_period("M")

monthly_revenue = merged.groupby("YearMonth")["Revenue"].sum()

print("=== Monthly Revenue Trend ===")
print(monthly_revenue)
print()

# ------------------------------------------------------------------
# Optional: export results to CSV for use in the dashboard step
# ------------------------------------------------------------------
top_products.to_csv("top_products_python.csv")
revenue_by_country.to_csv("revenue_by_country_python.csv")
monthly_revenue.to_csv("monthly_revenue_trend.csv")

print("Results exported to CSV.")

# ------------------------------------------------------------------
# Task 4 — Seasonal check: average revenue by calendar month
# (across all years, to see if a month is consistently high/low)
# ------------------------------------------------------------------
merged["Month"] = merged["OrderDate"].dt.month
merged["MonthName"] = merged["OrderDate"].dt.month_name()
 
seasonal_avg = (
    merged.groupby(["Month", "MonthName"])["Revenue"]
    .sum()
    .div(merged.groupby(["Month", "MonthName"])["YearMonth"].nunique())
    .sort_index()
)
 
print("=== Average Revenue by Calendar Month (across all years) ===")
print(seasonal_avg)
print()
 
seasonal_avg.to_csv("seasonal_avg_revenue.csv")
print("Seasonal averages exported to CSV.")
