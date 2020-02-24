class Response(object):
    def __init__(self, response):
        self.response = response

    def web_detection_serialize(self) -> list:
        raise NotImplementedError

    def logo_detection_serialize(self) -> list:
        raise NotImplementedError
