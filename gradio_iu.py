import gradio as gr
from structured_tools import agent_executor

def query_handler(query_string):
    source = agent_executor.invoke({
        "input": query_string,
        "chat_history": []
    })
    source_output = source['output']
    return source_output

interface = gr.Interface(
    fn=query_handler,
    inputs=gr.inputs.Textbox(lines=3, placeholder="Enter your query here..."),
    outputs=gr.outputs.Textbox(label="Query Output"),
    title="Query Processing App",
    description="Enter a query string to process it using the structured_tools agent_executor.",
)

if __name__ == "__main__":
    interface.launch()