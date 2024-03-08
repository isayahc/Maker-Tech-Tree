import gradio as gr
from weaviate_utils import init_client

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

from google_buckets import CloudStorageManager
import dotenv
import os

from utils import (
    change_file_extension, convert_obj_to_stl,
    remove_files
)

from mesh_utils import generate_mesh_images

from vision_model import analyze_images

from gradio_client import Client as ShapEClient

dotenv.load_dotenv()

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
    weaviate_client = init_client()
    app_components =  output_text["Material"]
    component_collection = weaviate_client.collections.get("Component")
    
    bucket_name = os.getenv('GOOGLE_BUCKET_NAME')
    
    bucket_name = os.getenv('GOOGLE_BUCKET_NAME')
    
    credentials_str = SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

    # Create an instance of CloudStorageManager
    manager = CloudStorageManager(bucket_name, credentials_str)
    
    
    for i in app_components:
        
        client = ShapEClient("hysts/Shap-E")
        client.hf_token = os.getenv("HUGGINGFACE_API_KEY")
        result = client.predict(
                i,	# str  in 'Prompt' Textbox component
                1621396601,	# float (numeric value between 0 and 2147483647) in 'Seed' Slider component
                15,	# float (numeric value between 1 and 20) in 'Guidance scale' Slider component
                64,	# float (numeric value between 2 and 100) in 'Number of inference steps' Slider component
                api_name="/text-to-3d"
        )

        app_uuid = component_collection.data.insert({
            "Tags": output_text['Fields_of_study'],
            "FeildsOfStudy" : output_text['Fields_of_study'],
            "ToolName" : i,
            "UsedInComps" : [input_text]
        })
        
        
        glb_file_name = app_uuid.hex + ".glb"
        
        manager.upload_file(
            result,
            glb_file_name,
            )
    
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

def search_experiments(input_text, number):
    # Example processing function
    weaviate_client = init_client()
    science_experiment_collection = weaviate_client.collections.get("ScienceEperiment")
    response = science_experiment_collection.query.bm25(
            query=input_text,
            limit=number
        )
    weaviate_client.close()
    response_objects_string = "\n\n".join([str(obj) for obj in response.objects])
    return response_objects_string

def search_apparatus(input_text, number):
    # Example processing function
    weaviate_client = init_client()
    component_collection = weaviate_client.collections.get("Component")
    response = component_collection.query.bm25(
            query=input_text,
            limit=number
        )
    # print(response.objects.__str__())
    response_objects_string = "\n\n".join([str(obj) for obj in response.objects])
    weaviate_client.close()
    
    return response_objects_string

def review_3d_model(uuid:str) -> None:
    """input the uuid of a 3d model"""
    uuid = uuid.replace("-","")
    bucket_name = os.getenv('GOOGLE_BUCKET_NAME')
    
    credentials_str = SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

    # Create an instance of CloudStorageManager
    manager = CloudStorageManager(bucket_name, credentials_str)
    xx = manager.get_file_by_uuid(uuid)
    manager.download_file(
        xx,
        xx
    )
    xx_as_stl = change_file_extension(xx,"stl")
    convert_obj_to_stl(xx,xx_as_stl)
    viewing_angles = [(30, 45), (60, 90), (45, 135)]
    
    prompt = "I am creating an 3d model ,\
    using a text-to-3d model\
    Do these images look correct?\
    If not please make a suggesttion on how to improve the text input"
    # As this response will be used in a pipeline please only output a new"  
    # potential prompt or output nothing, "
    # Please keep the prompt to 5 25 words to not confuse the model"
    
    images = generate_mesh_images(
        xx_as_stl,
        viewing_angles,
        
        )
    
    response = analyze_images(
        images, 
        prompt, 
        # api_key,
        )
    
    #clean up
    remove_files(images)
    remove_files([xx,xx_as_stl])
    return response
    
def download_3d_model(uuid:str):
    uuid = uuid.replace("-","")
    bucket_name = os.getenv('GOOGLE_BUCKET_NAME')
    
    credentials_str = SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

    # Create an instance of CloudStorageManager
    manager = CloudStorageManager(bucket_name, credentials_str)
    xx = manager.get_file_by_uuid(uuid)
    manager.download_file(
        xx,
        xx
    )
    return xx

generate_apparatus_interface = gr.Interface(
    fn=generate_apparatus,
    inputs=["text", gr.Radio(choices=list(apparatus_retriever_options.keys()), label="Select a retriever", value="Wikipedia")],
    outputs="text",
    title="Generate Apparatus",
    description="I am here to help makers make more and learn the science behind things. PLEASE NOTE: this call relies on HF calls so it may fail due to rate limits",
)

generate_experiment_interface = gr.Interface(
    fn=generate_experiment,
    inputs=["text", gr.Radio(choices=list(experiment_retriever_options.keys()), label="Select a retriever", value="Wikipedia")],
    outputs="text",
    title="Generate an experiment",
    description="I am here to generate and store science experiments for our users",
)

search_experiments_interface = gr.Interface(
    fn=search_experiments,
    inputs=["text", gr.Slider(minimum=2, maximum=6, step=1, value=2, label="Select a number")],
    outputs="text",
    title="Search Existing Experiments",
    description="If you would like an idea of the experiments in the vectorestore here is the place",
)

search_apparatus_interface = gr.Interface(
    fn=search_apparatus,
    inputs=["text", gr.Slider(minimum=2, maximum=6, step=1, value=2, label="Select a number")],
    outputs="text",
    title="Search Existing Apparatuses",
    description="If you would like an idea of the apparatuses in the vectorestore here is the place",
)

review_3d_model_interface = gr.Interface(
    fn=review_3d_model,
    inputs=["text"],
    outputs="text",
    title="Review 3D Model",
    description="Input the UUID of a 3D model to review its images and provide feedback.",
)

download_3d_model_interface = gr.Interface(
    fn=download_3d_model,
    inputs=["text"],
    outputs=gr.File(label="Input File"),
    title="Review 3D Model",
    description="Input the UUID of a 3D model to review its images and provide feedback.",
)


demo = gr.TabbedInterface([
    generate_apparatus_interface, 
    generate_experiment_interface,
    search_experiments_interface,
    search_apparatus_interface,
    review_3d_model_interface,
    download_3d_model_interface,
], [
    "Generate Apparatus",
    "Generate Experiment", 
    "Search Existing Experiments",
    "Search Existing Apparatuses",
    "review_3d_model_interface",
    "download_3d_model_interface"
    ])

if __name__ == "__main__":
    demo.launch()
