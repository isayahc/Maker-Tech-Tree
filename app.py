import gradio as gr

def get_secret(secret: str):
    return f"The secret you entered is: {secret}"

iface = gr.Interface(fn=get_secret, inputs="text", outputs="text", title="Secret Input", description="Enter your secret:")
iface.launch()
