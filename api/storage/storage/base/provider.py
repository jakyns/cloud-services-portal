class Provider(object):
    PROVIDER = None

    def set_bucket(self, bucket) -> None:
        self.bucket = bucket

    def request_upload(self, file_uri, file_path) -> object:
        raise NotImplementedError

    def request_delete(self, file_uri) -> bool:
        raise NotImplementedError
