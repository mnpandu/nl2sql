import pandas as pd
from sqlalchemy import create_engine

# ---------- 🔧 Configuration ----------
csv_path = "C:\\Users\\mnpan\\Downloads\\archive (3)\\claim_data.csv"  # Replace with your actual CSV path

db_user = "postgres"
db_pass = "postgres"
db_host = "localhost"
db_port = "5432"
db_name = "postgres"
table_name = "claims_data"

# ---------- 📥 Load CSV ----------
df = pd.read_csv(csv_path)

# Clean column names to make them SQL-safe
df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]

# ---------- 🚀 Connect to PostgreSQL ----------
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

# ---------- 🧾 Load Data to PostgreSQL ----------
df.to_sql(table_name, con=engine, if_exists="replace", index=False)

print(f"✅ Table '{table_name}' created and loaded successfully.")
