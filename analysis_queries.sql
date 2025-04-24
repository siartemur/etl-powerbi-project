-- analysis_queries.sql
-- Author: Şiar Yılmaz
-- Purpose: This file contains analytical SQL queries used for Power BI visualizations and reporting from the data warehouse (MSSQL).

----------------------------------------------------------------------------------------
-- 1. Top 5 customers with the highest number of orders
----------------------------------------------------------------------------------------
SELECT 
    c.FullName AS Customer,
    COUNT(o.OrderKey) AS TotalOrders
FROM FactOrder o
JOIN DimCustomer c ON o.CustomerKey = c.CustomerKey
GROUP BY c.FullName
ORDER BY TotalOrders DESC
OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;

-- Explanation:
-- Retrieves the top 5 customers based on order count, sorted descending.

----------------------------------------------------------------------------------------
-- 2. Top-selling products by quantity sold
----------------------------------------------------------------------------------------
SELECT 
    p.ProductName,
    SUM(o.Quantity) AS TotalQuantity
FROM FactOrder o
JOIN DimProduct p ON o.ProductKey = p.ProductKey
GROUP BY p.ProductName
ORDER BY TotalQuantity DESC;

-- Explanation:
-- Shows which products have the highest total units sold.

----------------------------------------------------------------------------------------
-- 3. Order count grouped by customer city
----------------------------------------------------------------------------------------
SELECT 
    c.City,
    COUNT(o.OrderKey) AS OrderCount
FROM FactOrder o
JOIN DimCustomer c ON o.CustomerKey = c.CustomerKey
GROUP BY c.City
ORDER BY OrderCount DESC;

-- Explanation:
-- Useful for regional sales analysis – shows where orders are coming from.

----------------------------------------------------------------------------------------
-- 4. Monthly order trends
----------------------------------------------------------------------------------------
SELECT 
    FORMAT(o.OrderDate, 'yyyy-MM') AS OrderMonth,
    COUNT(*) AS TotalOrders,
    SUM(o.Quantity) AS TotalUnits
FROM FactOrder o
GROUP BY FORMAT(o.OrderDate, 'yyyy-MM')
ORDER BY OrderMonth;

-- Explanation:
-- Aggregates orders and units sold by month – reveals seasonal trends.

----------------------------------------------------------------------------------------
-- 5. Orders grouped by payment method
----------------------------------------------------------------------------------------
SELECT 
    o.PaymentType,
    COUNT(*) AS OrderCount
FROM FactOrder o
GROUP BY o.PaymentType
ORDER BY OrderCount DESC;

-- Explanation:
-- Identifies which payment types are most frequently used by customers.

----------------------------------------------------------------------------------------
-- 6. Sales quantity grouped by product category
----------------------------------------------------------------------------------------
SELECT 
    cat.CategoryName,
    SUM(o.Quantity) AS TotalSold
FROM FactOrder o
JOIN DimProduct p ON o.ProductKey = p.ProductKey
JOIN DimCategory cat ON p.CategoryKey = cat.CategoryKey
GROUP BY cat.CategoryName
ORDER BY TotalSold DESC;

-- Explanation:
-- Provides insight into category-level product performance.
