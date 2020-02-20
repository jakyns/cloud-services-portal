from lib.storage import errors as StorageError

from api.storage.storage.gcp.provider import Provider as GCPProvider


class StorageService(object):
    def __init__(self, identifier):
        self.provider = self.__from_identifier(identifier)()

    def get_bucket(self) -> str:
        return self.provider.bucket

    def set_bucket(self, bucket: str) -> None:
        return self.provider.set_bucket(bucket)

    def request_retrieve(self, remote_file_path: str) -> dict:
        try:
            return self.provider.request_retrieve(remote_file_path)
        except StorageError.BucketNotFound:
            raise StorageError.BucketNotFound
        except StorageError.FileNotFound:
            raise StorageError.FileNotFound

    def request_upload(self, remote_file_path: str, local_file_path: str) -> dict:
        try:
            return self.provider.request_upload(remote_file_path, local_file_path)
        except StorageError.BucketNotFound:
            raise StorageError.BucketNotFound
        except StorageError.FileNotFound:
            raise StorageError.FileNotFound

    def request_delete(self, remote_file_path: str) -> dict:
        try:
            return self.provider.request_delete(remote_file_path)
        except StorageError.BucketNotFound:
            raise StorageError.BucketNotFound
        except StorageError.FileNotFound:
            raise StorageError.FileNotFound

    # private

    def __from_identifier(self, identifier: str):
        provider = self.__available_providers().get(identifier.lower(), None)

        if not provider:
            raise StorageError.ProviderNotFound(
                f"provider {identifier} is not available"
            )

        return provider

    def __available_providers(self):
        return {"gcp": GCPProvider}
