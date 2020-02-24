class Request(object):
    def detect_web(uri: str) -> object:
        raise NotImplementedError

    def detect_logo(uri: str) -> object:
        raise NotImplementedError
