import obs

from lib.storage import errors as StorageError


class Request:
    def __init__(self, client: obs.client.ObsClient, bucket: str):
        self.client = client
        self.bucket = bucket

    def retrieve(self, remote_file_path: str) -> obs.model.GetResult:
        return self.client.getObject(self.bucket, remote_file_path)
