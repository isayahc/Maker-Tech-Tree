import gradio as gr
from get_blender import main

main()

def process_text(input_text):
    # Your processing logic here
    return input_text.upper()

textbox = gr.Textbox(
    lines=5,
    placeholder="Type your text here...",
    interactive=False  # Set this to False to hide the input
)

interface = gr.Interface(
    fn=process_text,
    inputs=textbox,
    outputs="text"
)

interface.launch()
