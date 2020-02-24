from google import protobuf
from google.cloud import vision

from lib.ai import errors as AIError

from api.ai.vision.base.request import Request as BaseRequest


class Request(BaseRequest):
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def detect_web(
        self, uri: str
    ) -> protobuf.pyext._message.RepeatedCompositeContainer:
        image = self.__image_type(uri)
        web_entities_response = self.__web_entity_detection(image)

        return web_entities_response

    def detect_logo(
        self, uri: str
    ) -> protobuf.pyext._message.RepeatedCompositeContainer:
        image = self.__image_type(uri)
        logo_response = self.__logo_detection(image)

        return logo_response

    # private

    def __image_type(self, uri: str) -> vision.types.Image:
        image = vision.types.Image()
        image.source.image_uri = uri

        return image

    def __web_detection_annotations(
        self, image: vision.types.Image
    ) -> vision.types.AnnotateImageResponse:
        return self.client.web_detection(image=image)

    def __logo_detection_annotations(
        self, image: vision.types.Image
    ) -> vision.types.AnnotateImageResponse:
        return self.client.logo_detection(image=image)

    def __check_annotations(self, response: vision.types.AnnotateImageResponse) -> None:
        if response.error.message:
            raise AIError.FileObjectNotFound(response.error.message)

    def __web_entity_detection(
        self, image: vision.types.Image
    ) -> protobuf.pyext._message.RepeatedCompositeContainer:
        annotations_response = self.__web_detection_annotations(image)
        self.__check_annotations(annotations_response)

        return annotations_response.web_detection.web_entities

    def __logo_detection(
        self, image: vision.types.Image
    ) -> protobuf.pyext._message.RepeatedCompositeContainer:
        annotations_response = self.__logo_detection_annotations(image)
        self.__check_annotations(annotations_response)

        return annotations_response.logo_annotations
