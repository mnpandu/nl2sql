# config.py
import os

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
# PostGreSQL connection details
DB_DRIVER = "postgresql"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Business rules
INCLUDE_TABLES = ["claims_data"]
SAMPLE_ROWS = 3
SCHEMA = "public"
