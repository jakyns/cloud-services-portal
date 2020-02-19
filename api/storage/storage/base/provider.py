class Provider(object):
    PROVIDER = None

    def set_bucket(self, bucket) -> None:
        self.bucket = bucket

    def get_bucket(self, bucket) -> str:
        return self.bucket

    def request_retrieve(self, remote_file_path) -> dict:
        raise NotImplementedError

    def request_upload(self, remote_file_path, local_file_path) -> dict:
        raise NotImplementedError

    def request_delete(self, remote_file_path) -> dict:
        raise NotImplementedError
