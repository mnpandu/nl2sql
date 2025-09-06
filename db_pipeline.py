# db_pipeline.py
import openai
import pandas as pd
import logging
import oracledb
from langchain_community.utilities import SQLDatabase
from config import *
from db_utils import get_engine, get_db_connection
from sql_utils import build_prompt, clean_sql
from sqlalchemy.engine import URL
import sqlalchemy as sa

logger = logging.getLogger("NL2SQLPipeline")
logger.setLevel(logging.INFO)

openai.api_key = OPENAI_API_KEY

class NL2SQLPipeline:
    def create_db_context(self):
        engine = get_engine()
        db = SQLDatabase(
            engine,
            include_tables=INCLUDE_TABLES,
            sample_rows_in_table_info=SAMPLE_ROWS,
            schema=SCHEMA
        )
        return db.get_context()["table_info"]

    def text_to_sql(self, question):
            # Get database schema with sample rows
            schema_info = self.create_db_context()

            # Prompt for GPT
            prompt = build_prompt(schema_info, question)

            # Generate SQL using OpenAI
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            raw_output = response.choices[0].message.content.strip()           
            sql_query=clean_sql(raw_output)
            try:
                # Execute SQL on PostGreSQL
                conn=get_db_connection()
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