from api.storage.storage.gcp.provider import Provider as GCPProvider


class StorageService(object):
    def __init__(self, identifier):
        self.provider = self.__from_identifier(identifier)()

    def get_bucket(self) -> str:
        return self.provider.bucket

    def set_bucket(self, bucket) -> None:
        return self.provider.set_bucket(bucket)

    def request_upload(self, remote_file_path, local_file_path) -> dict:
        return self.provider.request_upload(remote_file_path, local_file_path)

    def request_delete(self, remote_file_path) -> dict:
        return self.provider.request_delete(remote_file_path)

    # private

    def __from_identifier(self, identifier):
        provider = self.__available_providers().get(identifier.lower(), None)

        if not provider:
            raise ValueError(f"provider {identifier} is not available")

        return provider

    def __available_providers(self):
        return {"gcp": GCPProvider}