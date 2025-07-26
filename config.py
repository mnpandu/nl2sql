# config.py
import os

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
