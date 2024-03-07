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

from weaviate_utils import init_client

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
    exp_data = output_text = selected_chain.invoke(input_text)
    
    weaviate_client = init_client()
    
    science_experiment_collection = weaviate_client.collections.get("ScienceEperiment")
    
    exp_uuid = science_experiment_collection.data.insert({
        # "DateCreated": datetime.now(timezone.utc),
        "FieldsOfStudy": exp_data['Fields_of_study'],
        "Tags": exp_data['Fields_of_study'],
        "Experiment_Name": exp_data['Experiment_Name'],
        "Material": exp_data['Material'],
        "Sources": exp_data['Sources'],
        "Protocal": exp_data['Protocal'],
        "Purpose_of_Experiments": exp_data['Purpose_of_Experiments'],
        "Safety_Precaution": exp_data['Safety_Precuation'],  # Corrected spelling mistake
        "Level_of_Difficulty": exp_data['Level_of_Difficulty'],
    })
    return output_text

def process_text(input_text, number):
    # Example processing function
    weaviate_client = init_client()
    science_experiment_collection = weaviate_client.collections.get("ScienceEperiment")
    response = science_experiment_collection.query.bm25(
            query=input_text,
            limit=3
        )
    return response.objects.__str__()

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

process_text_interface = gr.Interface(
    fn=process_text,
    inputs=["text", gr.Slider(minimum=2, maximum=6, step=1, value=2, label="Select a number")],
    outputs="text",
    title="Search Existing Experiments",
    description="If you would like an idea of the experiments in the vectorestore here is the place",
)

demo = gr.TabbedInterface([
    generate_apparatus_interface, 
    generate_experiment_interface,
    process_text_interface
], ["Generate Apparatus", "Generate Experiment", "Search Existing Experiments"])

if __name__ == "__main__":
    demo.launch()
