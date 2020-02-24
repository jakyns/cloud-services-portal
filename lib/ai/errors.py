class FileObjectNotFound(Exception):
    def __init__(self, message="File Object not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ProviderNotFound(Exception):
    def __init__(self, message="Provider not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
