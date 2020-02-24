class Provider(object):
    PROVIDER = None

    def request_web_detection(self, uri: str) -> list:
        raise NotImplementedError

    def request_logo_detection(self, uri: str) -> list:
        raise NotImplementedError
