# sql_utils.py
def build_prompt(schema_info, question):
    return f"""
            You are an Oracle SQL generator.
            ### Schema:
            {schema_info}
            ### User Question:
            {question}
            """

def clean_sql(raw_output: str):
    raw_output = raw_output.strip()
    if "```sql" in raw_output:
        sql_query = raw_output.split("```sql")[1].split("```")[0].strip()
    elif "```" in raw_output:
        sql_query = raw_output.split("```")[1].strip()
    else:
        lines = [line for line in raw_output.splitlines() if line.strip().lower().startswith("select")]
        sql_query = lines[0].strip() if lines else raw_output

    sql_query = sql_query.rstrip(";")
    return sql_query