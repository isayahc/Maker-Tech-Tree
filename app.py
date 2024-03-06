import gradio as gr
from structured_apparatus_chain import (
    arxiv_chain as apparatus_arxiv_chain, 
    pub_med_chain as apparatus_pub_med_chain, 
    wikipedia_chain as apparatus_wikipedia_chain
)
from structured_experiment_chain import (
    arxiv_chain as experiment_arxiv_chain, 
    pub_med_chain as experiment_pub_med_chain, 
    wikipedia_chain as experiment_wikipedia_chain
)

apparatus_retriever_options = {
    "Arxiv": apparatus_arxiv_chain,
    "PubMed": apparatus_pub_med_chain,
    "Wikipedia": apparatus_wikipedia_chain,
}

experiment_retriever_options = {
    "Arxiv": experiment_arxiv_chain,
    "PubMed": experiment_pub_med_chain,
    "Wikipedia": experiment_wikipedia_chain,
}

def generate_apparatus(input_text, retriever_choice):
    selected_chain = apparatus_retriever_options[retriever_choice]
    output_text = selected_chain.invoke(input_text)
    return output_text

def generate_experiment(input_text, retriever_choice):
    selected_chain = experiment_retriever_options[retriever_choice]
    output_text = selected_chain.invoke(input_text)
    return output_text

generate_apparatus_interface = gr.Interface(
    fn=generate_apparatus,
    inputs=["text", gr.Radio(choices=list(apparatus_retriever_options.keys()), label="Select a retriever", value="Wikipedia")],
    outputs="text",
    title="Generate Apparatus",
    description="I am here to help makers make more and learn the science behind things",
)

generate_experiment_interface = gr.Interface(
    fn=generate_experiment,
    inputs=["text", gr.Radio(choices=list(experiment_retriever_options.keys()), label="Select a retriever", value="Wikipedia")],
    outputs="text",
    title="Generate an experiment",
    description="I am here to generate and store science experiments for our users",
)

demo = gr.TabbedInterface([
    generate_apparatus_interface, 
    generate_experiment_interface,
], ["Generate Apparatus", "Generate Experiment"])

if __name__ == "__main__":
    demo.launch()
