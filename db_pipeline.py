# db_pipeline.py
import openai
import pandas as pd
import logging
import oracledb
from langchain_community.utilities import SQLDatabase
from config import *
from db_utils import get_engine, get_oracle_connection
from sql_utils import build_prompt, clean_sql
from sqlalchemy.engine import URL
import sqlalchemy as sa

logger = logging.getLogger("NL2SQLPipeline")
logger.setLevel(logging.INFO)

openai.api_key = OPENAI_API_KEY

class NL2SQLPipeline:
    def __init__(self):
        self.drivername = DB_DRIVER
        self.db_host = DB_HOST
        self.db_port = DB_PORT
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD

    def create_engine(self):
        # Create SQLAlchemy engine for Oracle using oracledb thin driver
        url = URL.create(
            drivername=self.drivername,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name
        )
        return sa.create_engine(url)

    def create_db_context(self):
        engine = self.create_engine()
        db = SQLDatabase(
            engine,
            include_tables=INCLUDE_TABLES,
            sample_rows_in_table_info=SAMPLE_ROWS,
            schema="C##MYAI"
        )
        return db.get_context()["table_info"]

    def text_to_sql(self, question):
            # Get database schema with sample rows
            schema_info = self.create_db_context()

            # Prompt for GPT
            prompt = f"""
            You are an Oracle SQL generator.
            ### Schema:
            {schema_info}
            ### User Question:
            {question}
            """

            # Generate SQL using OpenAI
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            raw_output = response.choices[0].message.content.strip()

            # ✅ Extract SQL inside the ```sql ... ``` block
            if "```sql" in raw_output:
                sql_query = raw_output.split("```sql")[1].split("```")[0].strip()
            elif "```" in raw_output:
                sql_query = raw_output.split("```")[1].strip()
            else:
                # fallback: find first line starting with SELECT
                lines = [line for line in raw_output.splitlines() if line.strip().lower().startswith("select")]
                sql_query = lines[0].strip() if lines else raw_output.strip()

            print(sql_query)
            sql_query = sql_query.rstrip(";")  # ✅ remove trailing semicolon

            try:
                # Execute SQL on Oracle
                conn = oracledb.connect(
                    user=self.db_user,
                    password=self.db_password,
                    dsn=f"{self.db_host}:{self.db_port}/{self.db_name}"
                )
                cursor = conn.cursor()
                cursor.execute(sql_query)
                cols = [c[0] for c in cursor.description]
                rows = cursor.fetchall()
                df = pd.DataFrame(rows, columns=cols)
                return sql_query, df if not df.empty else pd.DataFrame({"Info": ["✅ Query executed, no rows returned"]})

            except Exception as e:
                # Always return DataFrame to avoid Gradio crash
                return sql_query, pd.DataFrame({"Error": [f"❌ Error: {e}"]})

            finally:
                conn.close()    