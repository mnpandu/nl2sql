import gradio as gr
import pandas as pd
from db_pipeline2 import NL2SQLPipeline

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

# Examples
examples = [
    ["Show all employees"],
    ["List employees in Bangalore"],
    ["Who earns more than 5000"],
    ["Find all employees with salary between 4000 and 6000"],
    ["Show employees in Bangalore earning above 5000"],
    ["List employees where city is Chennai and salary is less than 7000"],
    ["Which employees are in the HR department"],
    ["Find employees in Engineering with salary greater than 6000"],
    ["Show employees with their department names"],
    ["List all employees and their departments in Bangalore"],
    ["Which department does Raj work in"],
    ["Show average salary for each department"],
    ["What is the highest salary"],
    ["What is the average salary in Engineering"],
    ["How many employees are in each city"],
    ["Count number of employees in Bangalore"],
    ["List employees ordered by salary descending"],
    ["Show top 3 highest paid employees"],
    ["Which employee has the lowest salary"],
    ["Find all employees with salary greater than the average salary"],
    ["Which city has the highest number of employees"],
    ["Show employees in Bangalore earning more than 5000 along with their department names"],
    ["Give me the staff working in Bangalore"],
    ["Employees making over 5K in Bangalore"],
    ["All HR employees in Mumbai"],
    ["Who are the top earners in Engineering"],
    ["Show me everyone earning more than 5000 with their city and department"],
    ["Total salary cost per department"],
    ["How many employees are there in the company"],
    ["Average salary by city"],
    ["Departments with employees in Bangalore"]
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
    gr.Markdown("## 🧠 NL2SQL Chatbot (Oracle)")
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
    iface.launch(share=True,server_name="0.0.0.0", server_port=7860)
