from google.cloud import storage
import os
import json

SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

# https://stackoverflow.com/questions/71878229/initializing-firebase-admin-via-environment-variables-without-storing-serviceacc
key_dict = json.loads(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)

SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')


# fire_app = firebase_admin.initialize_app(Certificate(key_dict))


# db = client = firestore.client(app=fire_app)
# Initialize Google Cloud Storage client
client = storage.Client()

# Define bucket and file name
# bucket_name = os.getenv('GOOGLE_PROJECT_ID')
bucket_name = "production-blender-platform-bucket"
# file_name = 'your-file.glb'
file_name = "tmpcpd7o7v0.glb"



# Function to upload a .glb file to the bucket
def upload_file(file_path):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_path)
    print(f'File {file_name} uploaded to {bucket_name}.')

# Function to download a .glb file from the bucket
def download_file(destination_path):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_path)
    print(f'File {file_name} downloaded to {destination_path}.')

# Function to delete a .glb file from the bucket
def delete_file():
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
    print(f'File {file_name} deleted from {bucket_name}.')

def main():
    # Example usage
    file_name = "tmpcpd7o7v0.glb"
    upload_file(file_name)
    download_file('path/to/save/your/file.glb')
    delete_file()

if __name__ == "__main__":
    main()
