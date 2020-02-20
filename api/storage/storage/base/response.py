class Response(object):
    def __init__(self, response):
        self.response = response

    def id(self) -> str:
        raise NotImplementedError

    def bucket(self) -> str:
        raise NotImplementedError

    def name(self) -> str:
        raise NotImplementedError

    def uri(self) -> str:
        raise NotImplementedError

    def public_url(self) -> str:
        raise NotImplementedError

    def exists(self) -> bool:
        raise NotImplementedError

    def serialize(self) -> dict:
        raise NotImplementedError
