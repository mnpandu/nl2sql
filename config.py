# config.py
import os

# Oracle connection details
DB_DRIVER = "oracle+oracledb"
DB_HOST = "localhost"
DB_PORT = 1521
DB_NAME = "FREE"
DB_USER = "C##MYAI"
DB_PASSWORD = "admin"

# Business rules
INCLUDE_TABLES = ["employees", "departments"]
SAMPLE_ROWS = 3
SCHEMA = "C##MYAI"
