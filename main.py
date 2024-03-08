# from langhchain_generate_components import maker_wikipedia_chain
from utils import (
    save_file, convert_obj_to_stl,
    change_file_extension, file_to_base64,
)
from mesh_utils import generate_mesh_images
from gradio_client import Client
from weaviate_utils import init_client
from datetime import datetime
from structured_apparatus_chain import (
    wikipedia_chain
)
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_APIKEY = os.getenv("OPENAI_API_KEY")
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")

def main():  
    # the object to be generated
    query = "A Microscope"
    
    # using a retriever we generat a list of Components
    output = wikipedia_chain.invoke(query)
    
    # the first item 
    shap_e_sample = output['Material'][0]
    shap_e_list = output['Fields_of_study']
    

    
    client = Client("hysts/Shap-E")
    client.hf_token = os.getenv("HUGGINGFACE_API_KEY")
    result = client.predict(
            shap_e_sample,	# str  in 'Prompt' Textbox component
            1621396601,	# float (numeric value between 0 and 2147483647) in 'Seed' Slider component
            15,	# float (numeric value between 1 and 20) in 'Guidance scale' Slider component
            64,	# float (numeric value between 2 and 100) in 'Number of inference steps' Slider component
            api_name="/text-to-3d"
    )
    
    weaviate_client = init_client()
    component_collection = weaviate_client.collections.get("Component")
    component_image_collection = weaviate_client.collections.get("ComponentImage")
    
    base_64_result = file_to_base64(result)
    
    uuid = component_collection.data.insert({
        "DateCreated" : datetime.now(timezone.utc),
        "UsedInComps" : [query],
        "ToolName" : shap_e_sample,
        "Tags" : shap_e_list,
        "feildsOfStudy" : shap_e_list,
        # "GlbBlob" : base_64_result,
    })
    
    
    
    
    
    saved_file_name = "sample.glb" 
    # save to local machine
    save_file(result,saved_file_name)
    
    stl_file_location = change_file_extension(
        saved_file_name,
        ".stl"
    )
    
    # convert into a stl without the texture
    # as it is easiest to handle
    convert_obj_to_stl(
        result, 
        stl_file_location,
        )
    
    # Need to generate screenshot for the item
    
    viewing_angles = [(30, 45), (60, 90), (45, 135)]
    
    # generate_mesh_images(
    #     stl_file_location, 
    #     viewing_angles
    #     )
    
    data_location = generate_mesh_images(
        stl_file_location,
        viewing_angles,
        "data",    
    )
    
    for item1, item2 in zip(data_location, viewing_angles):
    
        base_64_result = file_to_base64(item1)
    
        image_uuid = component_image_collection.data.insert({
            "DateCreated" : datetime.now(timezone.utc),
            "ImageAngle" : [str(i) for i in item2],
            "BelongsToComponent" : uuid,
        })
    
    
    
    # These screenshots need to be given to GPT-V
    # for feedback
    
    print(result)

    x = 0
    
if __name__ == "__main__":
    main()