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

from weaviate_utils import init_client

from datetime import datetime, timezone




def main():
    exp_qury = "fabricating cellolouse based electronics"
    exp_qury = "fabrication of spider silk"
    # app_query = "microscope"
    # app_data = apparatus_arxiv_chain.invoke(app_query)
    exp_data = experiment_arxiv_chain.invoke(exp_qury)
    
    weaviate_client = init_client()
    
    component_collection = weaviate_client.collections.get("Component")
    component_image_collection = weaviate_client.collections.get("ComponentImage")
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
