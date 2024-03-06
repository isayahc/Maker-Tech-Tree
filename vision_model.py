import base64
from openai import OpenAI
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

# source
# https://platform.openai.com/docs/guides/vision?lang=python
def analyze_images(
    images: List[str],
    prompt: str,
    # api_key: str,
    model: str = "gpt-4-vision-preview",
    max_tokens: int = 300
    ) -> Dict[str, Any]:
    """
    Analyze multiple images using OpenAI's vision model.

    Args:
        images (List[str]): List of URLs and/or local paths to the image files.
        prompt (str): Prompt message for the AI model.
        api_key (str): Your OpenAI API key.
        model (str, optional): Name of the vision model to use. Defaults to "gpt-4-vision-preview".
        max_tokens (int, optional): Maximum number of tokens for the response. Defaults to 300.

    Returns:
        dict: JSON response from the API.
    """
    client = OpenAI()
    messages = [{
        "role": "user",
        "content": [{"type": "text", "text": prompt}]
    }]

    for image in images:
        if image.startswith("http://") or image.startswith("https://"):
            # Image is a URL
            messages.append({
                "role": "user",
                "content": [{"type": "image_url", "image_url": {"url": image}}]
            })
        else:
            # Image is a local path
            with open(image, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            messages.append({
                "role": "user",
                "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]
            })

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0]

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    images = [
        "/workspaces/Maker-Tech-Tree/mesh_1.png",
        "/workspaces/Maker-Tech-Tree/mesh_2.png",
        "/workspaces/Maker-Tech-Tree/mesh_3.png",
    ]
    prompt = "I am creating an 3d model of a Glass lenses for refracting light,\
        using a text-to-3d model\
        Do these images look correct?\
        If not please make a suggesttion on how to improve the text input\
        As this response will be used in a pipeline please only output a new \
        potential prompt or output nothing, \
        Please keep the prompt to 5 25 words to not confuse the model"
    
    response = analyze_images(
        images, 
        prompt, 
        # api_key,
        )
    
    print(response)

if __name__ == "__main__":
    main()
