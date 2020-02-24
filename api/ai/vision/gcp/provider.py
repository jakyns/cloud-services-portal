from api.ai.vision.base.provider import Provider as BaseProvider

from api.ai.vision.gcp.request import Request as GCPRequest
from api.ai.vision.gcp.response import Response as GCPResponse


class Provider(BaseProvider):
    PROVIDER = "GCP"

    def request_web_detection(self, uri: str) -> list:
        request = GCPRequest()
        web_detection_response = request.detect_web(uri)

        response = GCPResponse(web_detection_response)

        return response.web_detection_serialize()

    def request_logo_detection(self, uri: str) -> list:
        request = GCPRequest()
        logo_detection_response = request.detect_logo(uri)

        response = GCPResponse(logo_detection_response)

        return response.logo_detection_serialize()
