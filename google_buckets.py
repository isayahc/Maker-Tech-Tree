from google.cloud import storage
import json
import os

class CloudStorageManager:
    def __init__(self, bucket_name, credentials_str):
        credentials_dict = json.loads(credentials_str)
        self.client = storage.Client.from_service_account_info(credentials_dict)
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
    # Replace 'your_bucket_name' with your actual bucket name
    bucket_name = os.getenv('GOOGLE_BUCKET_NAME')

    # Replace 'your_credentials_str' with your actual credentials string
    # credentials_str = """
    # {
    #     "type": "service_account",
    #     "project_id": "your_project_id",
    #     "private_key_id": "your_private_key_id",
    #     "private_key": "-----BEGIN PRIVATE KEY-----\nYourPrivateKey\n-----END PRIVATE KEY-----\n",
    #     "client_email": "your_client_email",
    #     "client_id": "your_client_id",
    #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #     "token_uri": "https://oauth2.googleapis.com/token",
    #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #     "client_x509_cert_url": "your_client_x509_cert_url"
    # }
    # """
    
    credentials_str = SERVICE_ACOUNT_STUFF = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

    # Create an instance of CloudStorageManager
    storage_manager = CloudStorageManager(bucket_name, credentials_str)

    # Example usage:
    # Upload a file
    storage_manager.upload_file('local_file_path', 'destination_file_name')

    # Download a file
    storage_manager.download_file('source_file_name', 'local_destination_path')

    # Delete a file
    storage_manager.delete_file('file_name_to_delete')

    # Get file by UUID
    uuid = 'your_uuid'
    file_name = storage_manager.get_file_by_uuid(uuid)
    if file_name:
        print(f"File with UUID '{uuid}' found: {file_name}")
    else:
        print(f"No file found with UUID '{uuid}'")


if __name__ == "__main__":
    main()
