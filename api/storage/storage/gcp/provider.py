from api.storage.storage.base.provider import Provider as BaseProvider

from api.storage.storage.gcp.request import Request as GCPRequest
from api.storage.storage.gcp.response import Response as GCPResponse


class Provider(BaseProvider):
    PROVIDER = "GCP"

    def set_bucket(self, bucket: str) -> None:
        self.bucket = bucket

    def get_bucket(self) -> str:
        return self.bucket

    def request_retrieve(self, remote_file_path: str) -> dict:
        request = GCPRequest(self.bucket)
        retrieve_response = request.retrieve(remote_file_path)

        response = GCPResponse(retrieve_response)

        return response.serialize()

    def request_upload(self, remote_file_path: str, local_file_path: str) -> dict:
        request = GCPRequest(self.bucket)
        upload_response = request.upload(remote_file_path, local_file_path)

        response = GCPResponse(upload_response)

        return response.serialize()

    def request_delete(self, remote_file_path: str) -> dict:
        request = GCPRequest(self.bucket)
        delete_response = request.delete(remote_file_path)

        response = GCPResponse(delete_response)

        return response.serialize()
