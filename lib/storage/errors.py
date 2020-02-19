class BucketNotFound(Exception):
    def __init__(self, message="Bucket not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class FileNotFound(Exception):
    def __init__(self, message="File not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ProviderNotFound(Exception):
    def __init__(self, message="Provider not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
