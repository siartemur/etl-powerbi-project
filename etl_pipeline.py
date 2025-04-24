import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
def load_dotenv_config():
    load_dotenv()
    return {
        "server": os.getenv("DB_SERVER"),
        "database": os.getenv("DB_NAME"),
        "auth_type": os.getenv("DB_AUTH"),
        "username": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

# Write ETL error logs to file
def log_error(category, message):
    with open("etl_errors.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{category}] {message}\n")

# Connect to MSSQL Server
config = load_dotenv_config()

if config["auth_type"] == "windows":
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"Trusted_Connection=yes;"
    )
else:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['username']};"
        f"PWD={config['password']};"
    )

cursor = conn.cursor()
print("✅ MSSQL connection successful.")

# ------------------------------------------
# 1. CUSTOMERS → DimCustomer
# ------------------------------------------
customers = pd.read_csv("seed_data/customers.csv")
customers["FullName"] = customers["first_name"] + " " + customers["last_name"]

print("📥 Loading customers...")
for _, row in customers.iterrows():
    try:
        if pd.isnull(row["email"]) or row["email"].strip() == "":
            raise ValueError(f"Missing email address: {row['FullName']}")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM DimCustomer WHERE CustomerKey = ?)
            INSERT INTO DimCustomer (CustomerKey, FullName, Email, City, SignupDate)
            VALUES (?, ?, ?, ?, ?)""",
            row["customer_id"], row["customer_id"], row["FullName"],
            row["email"], row["city"], row["signup_date"]
        )
    except Exception as e:
        log_error("CUSTOMER ERROR", str(e))

# ------------------------------------------
# 2. PRODUCTS & CATEGORIES → DimProduct, DimCategory
# ------------------------------------------
products = pd.read_csv("seed_data/products.csv")
categories = products["category_name"].drop_duplicates().reset_index(drop=True)

print("📦 Loading categories...")
for cat in categories:
    try:
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM DimCategory WHERE CategoryName = ?)
            INSERT INTO DimCategory (CategoryName) VALUES (?)""", cat, cat
        )
    except Exception as e:
        log_error("CATEGORY ERROR", str(e))

conn.commit()  # commit after loading categories

# Map CategoryKey
category_map = pd.read_sql("SELECT * FROM DimCategory", conn)
products = products.merge(category_map, how="left", left_on="category_name", right_on="CategoryName")

print("📦 Loading products...")
for _, row in products.iterrows():
    try:
        if pd.isnull(row["CategoryKey"]):
            raise ValueError(f"Category mapping failed: {row['product_name']}")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM DimProduct WHERE ProductKey = ?)
            INSERT INTO DimProduct (ProductKey, ProductName, Price, Stock, CategoryKey)
            VALUES (?, ?, ?, ?, ?)""",
            row["product_id"], row["product_id"], row["product_name"],
            row["price"], row["stock"], row["CategoryKey"]
        )
    except Exception as e:
        log_error("PRODUCT ERROR", str(e))

# ------------------------------------------
# 3. ORDERS → FactOrder
# ------------------------------------------
orders = pd.read_csv("seed_data/orders.csv")

print("🧾 Loading orders...")
for _, row in orders.iterrows():
    try:
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM FactOrder WHERE OrderKey = ?)
            INSERT INTO FactOrder (OrderKey, CustomerKey, ProductKey, Quantity, OrderDate, PaymentType, Status, UpdatedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            row["order_id"], row["order_id"], row["customer_id"],
            row["product_id"], row["quantity"], row["order_date"],
            row["payment_type"], row["status"], row["updated_at"]
        )
    except Exception as e:
        log_error("ORDER ERROR", str(e))

# ------------------------------------------
# COMMIT + CLOSE CONNECTION
# ------------------------------------------
conn.commit()
conn.close()
print("✅ All data successfully loaded.")
