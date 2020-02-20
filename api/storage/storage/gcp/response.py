from api.storage.storage.base.response import Response as BaseResponse


class Response(BaseResponse):
    def __init__(self, response):
        self.response = response

    def id(self) -> int:
        return self.response.id

    def bucket(self) -> str:
        return self.response.bucket.name

    def name(self) -> str:
        return self.response.name

    def public_url(self) -> str:
        return self.response.public_url

    def uri(self) -> str:
        return f"gs://{self.bucket()}/{self.name()}"

    def exists(self) -> bool:
        return self.response.exists()

    def serialize(self) -> dict:
        return {
            "id": self.id(),
            "bucket": self.bucket(),
            "name": self.name(),
            "public_url": self.public_url(),
            "uri": self.uri(),
            "exists": self.exists(),
        }
