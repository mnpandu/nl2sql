import gradio as gr
import pandas as pd
from db_pipeline import NL2SQLPipeline

# Initialize pipeline
pipeline = NL2SQLPipeline()

def handle_query(user_query):
    try:
        sql, result = pipeline.text_to_sql(user_query)
        return sql, result
    except Exception as e:
        return f"Error processing query: {str(e)}", pd.DataFrame()

# Clear function
def clear_all():
    return "", pd.DataFrame(), ""

# Examples Prompts
examples = [
    ["Show me all claims with their billed amount, allowed amount, and paid amount"],
    ["List all claims grouped by Claim Status (Paid, Denied, Under Review)"],
    ["Which claims are still in Pending AR Status"],
    ["Show the total billed vs. paid amount for all claims in the last 3 months"],
    ["Find all claims that are Partially Paid in Outcome"],
    ["List all claims submitted by a specific Provider ID"],
    ["Show providers with the highest number of denied claims"],
    ["Which providers have the largest billed amounts overall"],
    ["Find claims from providers that required Follow-up = Yes"],
    ["Compare allowed vs. paid amounts per provider"],
    ["Show all claims linked to a specific Patient ID"],
    ["Find patients with multiple denied claims"],
    ["Show claims where patients are on Self-Pay insurance type"],
    ["Which patients had the highest out-of-pocket difference (Billed – Paid)"],
    ["Show all claims per patient in a given date range"],
    ["Show claims submitted in August 2024"],
    ["Compare claims from Q2 vs. Q3 2024 by claim status"],
    ["List the top 10 highest billed claims in July 2024"],
    ["Show trend of paid claims month by month"],
    ["Find claims where service date was more than 90 days ago but still unresolved in AR"],
    ["Show claims where Paid Amount < 50% of Billed Amount"],
    ["Find claims denied due to 'Authorization not obtained'"],
    ["Show claims where Reason Code = Duplicate claim"],
    ["Identify claims with Follow-up Required = Yes and status = Denied"],
    ["Calculate the average reimbursement rate (Paid ÷ Allowed)"]
]


with gr.Blocks(css="""
#output-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}
#output-container .output-class {
    width: 70% !important;
    margin: auto;
    text-align: center;
}
""") as iface:
    gr.Markdown("## 🧠 NL2SQL Chatbot (PostGreSQL)")
    gr.Markdown("Ask natural language questions and get SQL + results from Oracle XE.")

    with gr.Row():
        question = gr.Textbox(label="Ask a question", placeholder="e.g. Show employees in Bangalore with salary > 5000")

    with gr.Column(elem_id="output-container"):
        sql_box = gr.Textbox(label="Generated SQL", elem_classes=["output-class"])
        result_df = gr.Dataframe(label="Query Results", wrap=True, elem_classes=["output-class"])

    with gr.Row():
        submit_btn = gr.Button("Submit")
        clear_btn = gr.Button("Clear")

    gr.Examples(examples=examples, inputs=question, examples_per_page=50)

    # Event bindings
    submit_btn.click(handle_query, inputs=question, outputs=[sql_box, result_df])
    clear_btn.click(clear_all, outputs=[sql_box, result_df, question])

if __name__ == "__main__":
    iface.launch(share=True,server_name="localhost", server_port=7860)
