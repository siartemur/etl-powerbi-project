import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv

# Load database credentials from .env
load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")

# MSSQL connection
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

# Retrieve top 5 customers by number of orders
def top_customers_by_orders():
    query = """
    SELECT TOP 5 c.FullName, COUNT(*) AS TotalOrders
    FROM FactOrder o
    JOIN DimCustomer c ON o.CustomerKey = c.CustomerKey
    GROUP BY c.FullName
    ORDER BY TotalOrders DESC;
    """
    df = pd.read_sql(query, conn)
    print("🧍‍♂️ Top 5 Customers by Total Orders:")
    print(df)

# Retrieve order distribution by city
def order_distribution_by_city():
    query = """
    SELECT c.City, COUNT(*) AS OrderCount
    FROM FactOrder o
    JOIN DimCustomer c ON o.CustomerKey = c.CustomerKey
    GROUP BY c.City
    ORDER BY OrderCount DESC;
    """
    df = pd.read_sql(query, conn)
    print("🌍 Order Distribution by City:")
    print(df)

# Run queries
if __name__ == "__main__":
    top_customers_by_orders()
    print("\n" + "-"*40 + "\n")
    order_distribution_by_city()
