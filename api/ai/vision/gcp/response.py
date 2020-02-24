from api.ai.vision.base.response import Response as BaseResponse


class Response(BaseResponse):
    def __init__(self, response):
        self.response = response

    def web_detection_serialize(self) -> list:
        return [{"label": res.description, "score": res.score} for res in self.response]

    def logo_detection_serialize(self) -> list:
        return [{"logo": res.description, "score": res.score} for res in self.response]
