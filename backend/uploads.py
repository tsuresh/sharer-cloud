from google.cloud import storage
from google.oauth2 import service_account

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # SOURCE:
    # https://cloud.google.com/storage/docs/uploading-objects#uploading-an-object

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    credentials = service_account.Credentials.from_service_account_file('./keys/sharer-cloud-dev-8ffaf64782ea.json')
    storage_client = storage.Client(project='sharer-cloud-dev', credentials=credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return destination_blob_name