from lib.ai import errors as AIError

from api.ai.vision.gcp.provider import Provider as GCPProvider


class VisionService(object):
    def __init__(self, identifier):
        self.provider = self.__from_identifier(identifier)()

    def request_web_detection(self, uri: str) -> list:
        try:
            return self.provider.request_web_detection(uri)
        except AIError.FileObjectNotFound:
            raise AIError.FileObjectNotFound

    def request_logo_detection(self, uri: str) -> list:
        try:
            return self.provider.request_logo_detection(uri)
        except AIError.FileObjectNotFound:
            raise AIError.FileObjectNotFound

    # private

    def __from_identifier(self, identifier: str) -> GCPProvider:
        provider = self.__available_providers().get(identifier.lower(), None)

        if not provider:
            raise AIError.ProviderNotFound(f"provider {identifier} is not available")

        return provider

    def __available_providers(self) -> dict:
        return {"gcp": GCPProvider}
