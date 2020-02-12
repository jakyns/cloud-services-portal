from google.cloud import storage
from google.cloud import exceptions

from lib.storage import errors as StorageError

from api.storage.storage.base.request import Request as BaseRequest


class Request(BaseRequest):
    def __init__(self, bucket):
        self.bucket = bucket

    def upload(self, remote_file_path, local_file_path) -> storage.blob.Blob:
        blob = self.__blob_object(remote_file_path)
        upload_obj = self.__upload_to_storage(blob, local_file_path)

        return upload_obj

    def delete(self, remote_file_path) -> storage.blob.Blob:
        blob = self.__blob_object(remote_file_path)
        delete_obj = self.__delete_from_storage(blob)

        return delete_obj

    # private

    def __storage_client(self) -> storage.blob:
        return storage.Client().get_bucket(self.bucket)

    def __blob_object(self, remote_file_path) -> storage.blob.Blob:
        try:
            storage_client = self.__storage_client()
            blob = storage_client.blob(remote_file_path)

            return blob
        except exceptions.NotFound as e:
            raise StorageError.BucketNotFound(e.message)

    def __upload_to_storage(self, blob, local_file_path) -> storage.blob.Blob:
        return blob.upload_from_filename(local_file_path)

    def __delete_from_storage(self, blob) -> storage.blob.Blob:
        if not blob.exists():
            raise StorageError.FileNotFound

        blob.delete()

        return blob
