from google.cloud import storage
from google.cloud import exceptions

from lib.storage import errors as StorageError

from api.storage.storage.base.request import Request as BaseRequest


class Request(BaseRequest):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def retrieve(self, remote_file_path: str) -> storage.blob.Blob:
        blob = self.__blob_object(remote_file_path)
        retrieve_obj = self.__retrieve_from_storage(blob, remote_file_path)

        return retrieve_obj

    def upload(self, remote_file_path: str, local_file_path: str) -> storage.blob.Blob:
        blob = self.__blob_object(remote_file_path)
        upload_obj = self.__upload_to_storage(blob, local_file_path)

        return upload_obj

    def delete(self, remote_file_path: str) -> storage.blob.Blob:
        blob = self.__blob_object(remote_file_path)
        delete_obj = self.__delete_from_storage(blob)

        return delete_obj

    # private

    def __storage_client(self) -> storage.blob:
        return storage.Client().get_bucket(self.bucket)

    def __blob_object(self, remote_file_path: str) -> storage.blob.Blob:
        try:
            storage_client = self.__storage_client()
            blob = storage_client.blob(remote_file_path)

            return blob
        except exceptions.NotFound as e:
            raise StorageError.BucketNotFound(e.message)

    def __check_existing(self, blob: storage.blob.Blob):
        if not blob.exists():
            raise StorageError.FileNotFound(
                f"{blob.name} object is not existed in GCP storage"
            )

    def __retrieve_from_storage(
        self, blob: storage.blob.Blob, remote_file_path: str
    ) -> storage.blob.Blob:
        self.__check_existing(blob)

        return blob

    def __upload_to_storage(
        self, blob: storage.blob.Blob, local_file_path: str
    ) -> storage.blob.Blob:
        try:
            blob.upload_from_filename(local_file_path)
        except FileNotFoundError:
            raise StorageError.FileNotFound("uploading file not found")

        return blob

    def __delete_from_storage(self, blob: storage.blob.Blob) -> storage.blob.Blob:
        self.__check_existing(blob)
        blob.delete()

        return blob
