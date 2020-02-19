from api.storage.storage.base.provider import Provider as BaseProvider

from api.storage.storage.gcp.request import Request as GCPRequest
from api.storage.storage.gcp.response import Response as GCPResponse


class Provider(BaseProvider):
    PROVIDER = "GCP"

    def set_bucket(self, bucket) -> None:
        self.bucket = bucket

    def get_bucket(self) -> str:
        return self.bucket

    def request_retrieve(self, remote_file_path) -> dict:
        request = GCPRequest(self.bucket)
        retrieve_response = request.retrieve(remote_file_path)

        response = self.__build_storage_response(retrieve_response)

        return {
            "id": response.id(),
            "bucket": response.bucket(),
            "name": response.name(),
            "public_url": response.public_url(),
            "exists": response.exists(),
        }

    def request_upload(self, remote_file_path, local_file_path) -> dict:
        request = GCPRequest(self.bucket)
        upload_response = request.upload(remote_file_path, local_file_path)

        response = self.__build_storage_response(upload_response)

        return {
            "id": response.id(),
            "bucket": response.bucket(),
            "name": response.name(),
            "public_url": response.public_url(),
            "exists": response.exists(),
        }

    def request_delete(self, remote_file_path) -> dict:
        request = GCPRequest(self.bucket)
        delete_response = request.delete(remote_file_path)

        response = self.__build_storage_response(delete_response)

        return {
            "id": response.id(),
            "bucket": response.bucket(),
            "name": response.name(),
            "public_url": response.public_url(),
            "exists": response.exists(),
        }

    # private

    def __build_storage_response(self, response) -> GCPResponse:
        return GCPResponse(response)
