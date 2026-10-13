import os
value = os.getenv("MY_VAR")
print(f"MY_VAR = {value}")

# Try reading a variable that's always set on Databricks
host = os.getenv("DATABRICKS_HOST")
print(f"DATABRICKS_HOST = {host}")