from weaviate_utils import init_client

def main():
    weaviate_client = init_client()
    component_collection = weaviate_client.collections.get("Component")
    response = component_collection.generate.near_text(
    query="biology",
    limit=2,
    grouped_task="Write a tweet with emojis about these facts."
)

    print(response.generated) 
    x = 0

if __name__ == '__main__':
    main()