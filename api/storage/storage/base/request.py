class Request(object):
    def __init__(self, bucket):
        self.bucket = bucket

    def retrieve(self, remote_file_path: str) -> object:
        raise NotImplementedError

    def upload(self, remote_file_path: str, local_file_path: str) -> object:
        raise NotImplementedError

    def delete(self, remote_file_path: str) -> object:
        raise NotImplementedError
