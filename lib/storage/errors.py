class BucketNotFound(Exception):
    def __init__(self, message="Bucket Not Found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class FileNotFound(Exception):
    def __init__(self, message="File Not Found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
