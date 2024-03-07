from google.cloud import storage

# Initialize Google Cloud Storage client
client = storage.Client()

# Define bucket and file name
bucket_name = 'your-bucket-name'
file_name = 'your-file.glb'

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
    upload_file('path/to/your/file.glb')
    download_file('path/to/save/your/file.glb')
    delete_file()

if __name__ == "__main__":
    main()
