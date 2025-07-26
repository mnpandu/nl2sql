# config.py
import os

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")

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
