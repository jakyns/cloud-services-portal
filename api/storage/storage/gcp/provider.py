from google.cloud import storage

from api.storage.storage.base.provider import Provider as BaseProvider

from api.storage.storage.gcp.bucket import Bucket


class Provider(BaseProvider):
    PROVIDER = "GCP"

    def set_bucket(self, bucket: str) -> None:
        self.bucket = Bucket(storage.Client(), bucket)

    def get_bucket(self) -> str:
        return self.bucket.name

    def request_retrieve(self, remote_file_path: str) -> dict:
        return self.bucket.retrieve(remote_file_path)

    def request_upload(self, remote_file_path: str, local_file_path: str) -> dict:
        return self.bucket.upload(remote_file_path, local_file_path)

    def request_delete(self, remote_file_path: str) -> dict:
        return self.bucket.delete(remote_file_path)
