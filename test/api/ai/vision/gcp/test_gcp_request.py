import unittest
import mock

from google.cloud import vision

from lib.ai import errors as AIError

from api.ai.vision.gcp.request import Request as GCPRequest


class TestAIVisionGCPRequest(unittest.TestCase):
    def setUp(self):
        self.request = GCPRequest()

    @mock.patch.object(GCPRequest, "_Request__web_detection_annotations")
    def test_that_raises_file_object_not_found_when_it_has_error_response_in_web_annotations_response(
        self, mock_annotations_response: mock.MagicMock
    ):
        mock_image_type = self.__mock_image_type()
        mock_error_response = self.__mock_detect_error_response()

        mock_annotations_response.return_value = mock_error_response

        with self.assertRaises(AIError.FileObjectNotFound):
            self.request.detect_web(self.uri())

        mock_annotations_response.assert_called_once_with(mock_image_type)

    @mock.patch.object(GCPRequest, "_Request__web_entity_detection")
    def test_that_returns_proper_response_when_it_can_detect_web_entity(
        self, mock_web_entity: mock.MagicMock
    ):
        mock_image_type = self.__mock_image_type()
        mock_web_entity_response = self.__mock_web_entity_response()

        mock_web_entity.return_value = mock_web_entity_response

        response = self.request.detect_web(self.uri())

        mock_web_entity.assert_called_once_with(mock_image_type)

        self.assertEqual("a1", response.web_detection.web_entities[0].get("entity_id"))
        self.assertEqual(0.99, response.web_detection.web_entities[0].get("score"))
        self.assertEqual("a2", response.web_detection.web_entities[1].get("entity_id"))
        self.assertEqual(0.50, response.web_detection.web_entities[1].get("score"))

    @mock.patch.object(GCPRequest, "_Request__logo_detection")
    def test_that_returns_proper_response_when_it_can_detect_logo(
        self, mock_logo: mock.MagicMock
    ):
        mock_image_type = self.__mock_image_type()
        mock_logo_response = self.__mock_logo_response()

        mock_logo.return_value = mock_logo_response

        response = self.request.detect_logo(self.uri())

        mock_logo.assert_called_once_with(mock_image_type)

        self.assertEqual("l1", response.web_detection.web_entities[0].get("mid"))
        self.assertEqual(0.97, response.web_detection.web_entities[0].get("score"))
        self.assertEqual("l2", response.web_detection.web_entities[1].get("mid"))
        self.assertEqual(0.60, response.web_detection.web_entities[1].get("score"))

    # static

    @staticmethod
    def uri() -> str:
        return "gs://bucket/file.txt"

    # private

    def __mock_image_type(self) -> vision.types.Image:
        obj = vision.types.Image()
        obj.source.image_uri = self.uri()

        return obj

    def __mock_detect_error_response(self) -> mock.MagicMock:
        obj = mock.Mock()
        obj.error.message = "error"

        return obj

    def __mock_web_entity_response(self) -> mock.MagicMock:
        obj = mock.Mock()
        obj.web_detection.web_entities = [
            {"entity_id": "a1", "score": 0.99, "description": "desc"},
            {"entity_id": "a2", "score": 0.50, "description": "desc2"},
        ]

        return obj

    def __mock_logo_response(self) -> mock.MagicMock:
        obj = mock.Mock()
        obj.web_detection.web_entities = [
            {"mid": "l1", "score": 0.97, "description": "desc"},
            {"mid": "l2", "score": 0.60, "description": "desc2"},
        ]

        return obj
