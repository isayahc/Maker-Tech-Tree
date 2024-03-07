from google.cloud import storage
import os
import json



from google.cloud import storage

class CloudStorageManager:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket_name = bucket_name

    def upload_file(self, file_path, destination_file_name):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_file_name)
        blob.upload_from_filename(file_path)
        print(f'File {destination_file_name} uploaded to {self.bucket_name}.')

    def download_file(self, source_file_name, destination_path):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(source_file_name)
        blob.download_to_filename(destination_path)
        print(f'File {source_file_name} downloaded to {destination_path}.')

    def delete_file(self, file_name):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.delete()
        print(f'File {file_name} deleted from {self.bucket_name}.')
        
    def get_file_by_uuid(self, uuid):
        bucket = self.client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=uuid)
        for blob in blobs:
            if blob.name.endswith('.glb'):
                return blob.name
        return None

def main():
    SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

    # https://stackoverflow.com/questions/71878229/initializing-firebase-admin-via-environment-variables-without-storing-serviceacc
    key_dict = json.loads(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
    )

    SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')


    # fire_app = firebase_admin.initialize_app(Certificate(key_dict))


    # Initialize Google Cloud Storage client
    client = storage.Client()
    bucket_name = os.getenv('GOOGLE_BUCKET_NAME')
    manager = CloudStorageManager(bucket_name)
    
    
    # uuid = '9ca1555c-e8ca-4111-a084-1a2374b2e6bd'
    # uuid = '9ca1555c-e8ca-4111-a084-1a2374b2e6bd'.replace("-","")
    uuid = "506bb34a122a4bea86a64f96933f6bbd"
    xx = manager.get_file_by_uuid(uuid)
    
    # manager.upload_file(
    #     "506bb34a122a4bea86a64f96933f6bbd.glb",
    #     "506bb34a122a4bea86a64f96933f6bbd.glb"
    # )
    
    manager.download_file(
        xx,
        xx
    )
    x = 0

    # Example usage
    # manager.upload_file("/home/isayahc/projects/Hackathon-Projects/Maker-Tech-Tree/7698996e43bf4aa1ba98f5dd0bf77000.glb", "7698996e43bf4aa1ba98f5dd0bf77000.glb")
    # manager.download_file('your-file.glb', 'path/to/save/your/file.glb')
    # manager.delete_file('your-file.glb')

if __name__ == "__main__":
    main()
