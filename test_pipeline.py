import pyodbc
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")

# Connect to MSSQL
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Test 1: Connection test
print("✅ [TEST 1] MSSQL connection successful.")

# Test 2: Check data presence in DimCustomer
cursor.execute("SELECT COUNT(*) FROM DimCustomer;")
row_count = cursor.fetchone()[0]
if row_count > 0:
    print(f"✅ [TEST 2] DimCustomer table contains {row_count} rows.")
else:
    print("❌ [TEST 2] DimCustomer table is empty!")

# Test 3: Check for data quality errors in etl_errors.log
if os.path.exists("etl_errors.log"):
    with open("etl_errors.log", "r", encoding="utf-8") as log_file:
        lines = [line for line in log_file if line.strip() and not line.strip().startswith("#")]
        if len(lines) == 0:
            print("✅ [TEST 3] etl_errors.log is clean. 🧼")
        else:
            print("❌ [TEST 3] etl_errors.log contains data quality issues!")
            for line in lines:
                print(line.strip())
else:
    print("❌ [TEST 3] etl_errors.log file not found!")
