import os
from dotenv import load_dotenv

import weaviate.classes as wvcc
import weaviate
from weaviate.classes.config import Property, DataType
import weaviate.classes as wvc

load_dotenv()


def init_client():
    """connects to data base
    source: https://weaviate.io/developers/weaviate/tutorials/connect
    """
    client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("YOUR_WCS_URL"),  # Set this environment variable
    auth_credentials=weaviate.auth.AuthApiKey(
        os.getenv("YOUR_WCS_AUTH_KEY")
    ),  # Set this environment variable
    headers={
        "X-OpenAI-Api-Key": os.environ[
            "OPENAI_API_KEY"
        ]  # Replace with your inference API key
    },
    )
    return client



x = 0
def main() :
    try:
        client = init_client()
        client.collections.create(
        name="Component",
        description="Component of a given Apparatus",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        properties=[
            # wvc.config.Property(name="id", data_type=wvc.config.DataType.UUID),
            wvc.config.Property(name="DateCreated", data_type=wvc.config.DataType.DATE),
            wvc.config.Property(name="UsedInComps", data_type=wvc.config.DataType.TEXT_ARRAY),
            wvc.config.Property(name="FeildsOfStudy", data_type=wvc.config.DataType.TEXT_ARRAY),
            wvc.config.Property(name="ToolName", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="Tags", data_type=wvc.config.DataType.TEXT_ARRAY),
            wvc.config.Property(name="GlbBlob", data_type=wvc.config.DataType.BLOB),
        ]
        )
    finally:
        client.close()

    try:
        client = init_client()
        client.collections.create(
        name="ScienceExperiment",
        description="Science Experiment with the goal of making something",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        properties=[
        wvc.config.Property(name="DateCreated", data_type=wvc.config.DataType.DATE),
        wvc.config.Property(name="UsedInComps", data_type=wvc.config.DataType.TEXT_ARRAY),
        wvc.config.Property(name="FieldsOfStudy", data_type=wvc.config.DataType.TEXT_ARRAY),
        wvc.config.Property(name="Experiment_Name", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="Material", data_type=wvc.config.DataType.TEXT_ARRAY),
        wvc.config.Property(name="Sources", data_type=wvc.config.DataType.TEXT_ARRAY),
        wvc.config.Property(name="Protocal", data_type=wvc.config.DataType.TEXT_ARRAY),
        wvc.config.Property(name="Purpose_of_Experiments", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="Safety_Precaution", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="Level_of_Difficulty", data_type=wvc.config.DataType.TEXT),
    ]
)
    finally:
        client.close()

    try:
        client = init_client()
        client.collections.create(
        name="ComponentImage",
        description="An image to gain visual context on a component",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        properties=[
            # wvc.config.Property(name="id", data_type=wvc.config.DataType.UUID),
            wvc.config.Property(name="DateCreated", data_type=wvc.config.DataType.DATE),
            wvc.config.Property(name="ImageContent", data_type=wvc.config.DataType.BLOB),
            wvc.config.Property(name="ImageAngle", data_type=wvc.config.DataType.TEXT_ARRAY),
            wvc.config.Property(name="BelongsToComponent", data_type=wvc.config.DataType.UUID),
        ]
    )
    finally:
        client.close()



def main():
    pass

if __name__ == '__main__':
    x = 0