# goal: store results from app.py into vector store

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


# from google_buckets import upload_file, man

from weaviate_utils import init_client

from datetime import datetime, timezone

from gradio_client import Client as ShapEClient
import os

from google_buckets import CloudStorageManager

from utils import copy_file_to_location

def main():
    # exp_qury = "fabricating cellolouse based electronics"
    # exp_qury = "fabrication of spider silk"
    # app_query = "microscope"
    # app_query = "A gas Condenser"
    app_query = "Electron Microscope"
    app_data = apparatus_arxiv_chain.invoke(app_query)
    # exp_data = experiment_arxiv_chain.invoke(exp_qury)
    
    weaviate_client = init_client()
    
    component_collection = weaviate_client.collections.get("Component")
    component_image_collection = weaviate_client.collections.get("ComponentImage")
    science_experiment_collection = weaviate_client.collections.get("ScienceEperiment")
    
    
    bucket_name = os.getenv('GOOGLE_BUCKET_NAME')
    manager = CloudStorageManager(bucket_name)
    
    
    
    app_components =  app_data["Material"]
    
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
            "Tags": app_data['Fields_of_study'],
            "FeildsOfStudy" : app_data['Fields_of_study'],
            "ToolName" : i,
            "UsedInComps" : [app_query]
        })
        
        glb_file_name = app_uuid.hex + ".glb"
        
        manager.upload_file(
            result,
            glb_file_name,
            )
        # copy_file_to_location(result,glb_file_name)
        # upload_file(glb_file_name)
        # os.remove(glb_file_name)
        
        x = 0
    
    response = component_collection.query.bm25(
            query="something that goes in a microscope",
            limit=5
        )
    
    # exp_uuid = science_experiment_collection.data.insert({
    #     # "DateCreated": datetime.now(timezone.utc),
    #     "FieldsOfStudy": exp_data['Fields_of_study'],
    #     "Tags": exp_data['Fields_of_study'],
    #     "Experiment_Name": exp_data['Experiment_Name'],
    #     "Material": exp_data['Material'],
    #     "Sources": exp_data['Sources'],
    #     "Protocal": exp_data['Protocal'],
    #     "Purpose_of_Experiments": exp_data['Purpose_of_Experiments'],
    #     "Safety_Precaution": exp_data['Safety_Precuation'],  # Corrected spelling mistake
    #     "Level_of_Difficulty": exp_data['Level_of_Difficulty'],
    # })
    
    response = science_experiment_collection.query.bm25(
            query="silk",
            limit=3
        )
    
    jj = science_experiment_collection.query.near_text(
        query="biology",
        limit=2
    )
    
    
    
    # uuid = component_collection.data.insert({
    #     "DateCreated" : datetime.now(timezone.utc),
    #     "UsedInComps" : [query],
    #     "ToolName" : shap_e_sample,
    #     "Tags" : shap_e_list,
    #     "feildsOfStudy" : shap_e_list,
    #     # "GlbBlob" : base_64_result,
    # })
    
    x = 0

if __name__ == '__main__':
    main()
