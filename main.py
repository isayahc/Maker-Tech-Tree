from langhchain_generate_components import maker_wikipedia_chain
from utils import (
    save_file, convert_obj_to_stl,
    change_file_extension,
)
from mesh_utils import generate_mesh_images
from gradio_client import Client


def main():  
    # the object to be generated
    query = "A Microscope"
    
    # using a retriever we generat a list of Components
    output = maker_wikipedia_chain.invoke(query)
    
    # the first item 
    shap_e_sample = output['Material'][0]
    
    client = Client("hysts/Shap-E")
    result = client.predict(
            shap_e_sample,	# str  in 'Prompt' Textbox component
            1621396601,	# float (numeric value between 0 and 2147483647) in 'Seed' Slider component
            15,	# float (numeric value between 1 and 20) in 'Guidance scale' Slider component
            64,	# float (numeric value between 2 and 100) in 'Number of inference steps' Slider component
            api_name="/text-to-3d"
    )
    
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
    
    generate_mesh_images(
        stl_file_location, 
        viewing_angles
        )
    
    # These screenshots need to be given to GPT-V
    # for feedback
    
    print(result)

    x = 0
    
if __name__ == "__main__":
    main()