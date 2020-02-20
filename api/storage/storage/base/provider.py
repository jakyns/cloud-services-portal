class Provider(object):
    PROVIDER = None

    def set_bucket(self, bucket: str) -> None:
        self.bucket = bucket

    def get_bucket(self, bucket: str) -> str:
        return self.bucket

    def request_retrieve(self, remote_file_path: str) -> dict:
        raise NotImplementedError

    def request_upload(self, remote_file_path: str, local_file_path: str) -> dict:
        raise NotImplementedError

    def request_delete(self, remote_file_path: str) -> dict:
        raise NotImplementedError
