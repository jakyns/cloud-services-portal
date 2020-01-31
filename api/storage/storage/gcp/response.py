from api.storage.storage.base.response import Response


class Response(Response):
    def __init__(self, response):
        self.response = response

    def id(self) -> int:
        return self.response.id

    def bucket(self) -> str:
        return self.response.bucket

    def name(self) -> str:
        return self.response.name

    def public_url(self) -> str:
        return self.response.public_url

    def exists(self) -> bool:
        return self.response.exists()
