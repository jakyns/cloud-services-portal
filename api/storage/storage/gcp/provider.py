from google.cloud import storage
from google.cloud import exceptions

from api.storage.storage.base.provider import Provider as BaseProvider
from api.storage.storage.gcp.response import Response as GCPResponse


class Provider(BaseProvider):
    PROVIDER = "GCP"

    def set_bucket(self, bucket) -> None:
        self.bucket = bucket

    def request_upload(self, remote_file_path, local_file_path) -> dict:
        file_object = self.__upload(remote_file_path, local_file_path)
        response = self.__build_storage_response(file_object)

        return {
            "id": response.id(),
            "bucket": response.bucket(),
            "name": response.name(),
            "public_url": response.public_url(),
            "exists": response.exists(),
        }

    def request_delete(self, remote_file_path) -> dict:
        file_object = self.__delete(remote_file_path)
        response = self.__build_storage_response(file_object)

        return {
            "id": response.id(),
            "bucket": response.bucket(),
            "name": response.name(),
            "public_url": response.public_url(),
            "exists": response.exists(),
        }

    # private

    def __storage_client(self) -> storage.blob:
        return storage.Client().get_bucket(self.bucket)

    def __blob_object(self, remote_file_path) -> storage.blob.Blob:
        try:
            storage_client = self.__storage_client()
            blob = storage_client.blob(remote_file_path)

            return blob
        except exceptions.NotFound as e:
            # TODO: raise our own error message here
            raise ValueError(e.message)

    def __upload(self, remote_file_path, local_file_path) -> storage.blob.Blob:
        blob = self.__blob_object(remote_file_path)
        blob.upload_from_filename(local_file_path)

        return blob

    def __delete(self, remote_file_path) -> storage.blob.Blob:
        blob = self.__blob_object(remote_file_path)

        if not blob.exists():
            # TODO: raise our own error message here
            raise ValueError

        blob.delete()

        return blob

    def __build_storage_response(self, response) -> GCPResponse:
        return GCPResponse(response)
