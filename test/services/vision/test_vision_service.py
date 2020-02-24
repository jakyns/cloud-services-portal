import unittest
import mock

from lib.ai import errors as AIError

from api.ai.vision.gcp.provider import Provider as GCPProvider

from services.vision import VisionService


class TestAIVisionService(unittest.TestCase):
    def setUp(self):
        self.service = VisionService("GCP")

    def test_that_raises_error_when_initialize_provider_which_is_not_available(self):
        with self.assertRaises(AIError.ProviderNotFound):
            VisionService("abcde")

    def test_that_can_initiate_provider(self):
        self.assertIsInstance(self.service, VisionService)
        self.assertIsInstance(self.service.provider, GCPProvider)

    @mock.patch.object(GCPProvider, "request_web_detection")
    def test_that_raises_file_object_not_found_when_file_is_not_existed(
        self, mock_request: mock.MagicMock
    ):
        mock_request.side_effect = AIError.FileObjectNotFound

        with self.assertRaises(AIError.FileObjectNotFound):
            self.service.request_web_detection(self.uri())

        mock_request.assert_called_once_with(self.uri())

    @mock.patch.object(GCPProvider, "request_web_detection")
    def test_that_can_request_web_detection(self, mock_response: mock.MagicMock):
        mock_response.return_value = self.__mock_vision_web_detection_response()

        response = self.service.request_web_detection(self.uri())

        mock_response.assert_called_once_with(self.uri())

        self.assertEqual(0.99, response[0].get("score"))
        self.assertEqual("desc", response[0].get("label"))
        self.assertEqual(0.50, response[1].get("score"))
        self.assertEqual("desc2", response[1].get("label"))

    @mock.patch.object(GCPProvider, "request_logo_detection")
    def test_that_can_request_logo_detection(self, mock_response: mock.MagicMock):
        mock_response.return_value = self.__mock_vision_logo_detection_response()

        response = self.service.request_logo_detection(self.uri())

        mock_response.assert_called_once_with(self.uri())

        self.assertEqual(0.97, response[0].get("score"))
        self.assertEqual("desc", response[0].get("logo"))
        self.assertEqual(0.60, response[1].get("score"))
        self.assertEqual("desc2", response[1].get("logo"))

    # static

    @staticmethod
    def uri() -> str:
        return "gs://bucket/file.txt"

    # private

    def __mock_vision_web_detection_response(self) -> list:
        return [{"score": 0.99, "label": "desc"}, {"score": 0.50, "label": "desc2"}]

    def __mock_vision_logo_detection_response(self) -> list:
        return [{"score": 0.97, "logo": "desc"}, {"score": 0.60, "logo": "desc2"}]
