from google.cloud import storage
from google.cloud import exceptions

from lib.storage import errors as StorageError

from api.storage.storage.gcp.blob_request import BlobRequest
from api.storage.storage.gcp.blob_response import BlobResponse


class Bucket(object):
    def __init__(self, storage_client: storage.client.Client, bucket: str):
        self.client = self.__initialize_bucket(storage_client, bucket)
        self.bucket = bucket

    def name(self) -> str:
        return self.bucket

    def retrieve(self, remote_file_path: str) -> dict:
        blob = BlobRequest(self.client, remote_file_path)
        blob.is_existed()

        response = BlobResponse(blob)

        return response.serialize()

    def upload(self, remote_file_path: str, local_file_path: str) -> dict:
        blob = BlobRequest(self.client, remote_file_path)
        blob.upload(local_file_path)

        response = BlobResponse(blob)

        return response.serialize()

    def delete(self, remote_file_path: str) -> dict:
        blob = BlobRequest(self.client, remote_file_path)
        blob.is_existed()
        blob.delete()

        response = BlobResponse(blob)

        return response.serialize()

    # private

    def __initialize_bucket(
        self, storage_client: storage.client.Client, bucket: str
    ) -> storage.bucket.Bucket:
        try:
            return storage_client.get_bucket(bucket)
        except exceptions.NotFound as e:
            raise StorageError.BucketNotFound(e.message)
