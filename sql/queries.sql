-- ============================================================
-- Northwind Sales Analysis — SQL Queries
-- Database: northwind.db (SQLite)
-- ============================================================

-- Q1: Warm-up join — attach customer details to each order
-- Purpose: confirm join logic between Orders and Customers
SELECT o.OrderID, c.CompanyName, c.Country, o.OrderDate
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
LIMIT 10;


-- Q2: Three-way join — order line items with product detail
-- Purpose: link Orders -> Order Details (bridge table) -> Products
-- This is the core pattern reused in Q3 below.
SELECT o.OrderID, p.ProductName, od.Quantity, od.UnitPrice
FROM Orders o
JOIN "Order Details" od ON o.OrderID = od.OrderID
JOIN Products p ON od.ProductID = p.ProductID
LIMIT 10;


-- Q3: Business question — which products generate the most revenue?
-- Purpose: identify top-performing products by total revenue
SELECT p.ProductName,
       SUM(od.Quantity * od.UnitPrice) AS Revenue
FROM "Order Details" od
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY Revenue DESC
LIMIT 10;


-- Q4: Business question — which countries generate the most revenue?
-- Purpose: identify top markets by total revenue
SELECT c.Country,
       SUM(od.Quantity * od.UnitPrice) AS Revenue
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.Country
ORDER BY Revenue DESC;


-- ============================================================
-- Data Quality Investigation
-- Triggered by: Q4 returning a NULL/blank row for Country
-- ============================================================

-- Q5: How many orders are affected by missing country data?
SELECT COUNT(*) AS orders_missing_country
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE c.Country IS NULL OR c.Country = '';

-- Q6: Is the issue at the customer level (blank field) or a broken join?
SELECT COUNT(*) AS customers_missing_country
FROM Customers
WHERE Country IS NULL OR Country = '';

-- Q7: Confirm no orders are orphaned (i.e. every order maps to a real customer)
SELECT COUNT(*) AS orphaned_orders
FROM Orders o
LEFT JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;

-- Finding: 335 orders (~2% of 16,282 total) had missing country data,
-- traced to 2 customer records with blank Country fields.
-- No orphaned orders — every order matches a real customer, so this
-- is a genuine missing-value issue rather than a broken relationship.
-- Recommendation: make Country a mandatory field at data entry.
