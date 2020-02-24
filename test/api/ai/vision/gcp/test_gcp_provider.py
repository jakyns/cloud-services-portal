import unittest
import mock

from lib.ai import errors as AIError

from api.ai.vision.gcp.provider import Provider as GCPProvider
from api.ai.vision.gcp.request import Request as GCPRequest


class TestAIVisionGCPProvider(unittest.TestCase):
    def setUp(self):
        self.provider = GCPProvider()

    @mock.patch.object(GCPRequest, "detect_web")
    def test_that_raises_file_object_not_found_when_requesting_to_gcp_service_is_error(
        self, mock_request: mock.MagicMock
    ):
        mock_request.side_effect = AIError.FileObjectNotFound

        with self.assertRaises(AIError.FileObjectNotFound):
            self.provider.request_web_detection(self.uri())

        mock_request.assert_called_once_with(self.uri())

    @mock.patch.object(GCPRequest, "detect_web")
    def test_that_can_request_web_detection_from_gcp_service(
        self, mock_request: mock.MagicMock
    ):
        mock_request.return_value = self.__mock_web_detection_response()

        response = self.provider.request_web_detection(self.uri())

        mock_request.assert_called_once_with(self.uri())

        self.assertEqual(0.99, response[0].get("score"))
        self.assertEqual("desc", response[0].get("label"))
        self.assertEqual(0.50, response[1].get("score"))
        self.assertEqual("desc2", response[1].get("label"))

    @mock.patch.object(GCPRequest, "detect_logo")
    def test_that_can_request_logo_detection_from_gcp_service(
        self, mock_request: mock.MagicMock
    ):
        mock_request.return_value = self.__mock_logo_detection_response()

        response = self.provider.request_logo_detection(self.uri())

        mock_request.assert_called_once_with(self.uri())

        self.assertEqual(0.97, response[0].get("score"))
        self.assertEqual("desc", response[0].get("logo"))
        self.assertEqual(0.60, response[1].get("score"))
        self.assertEqual("desc2", response[1].get("logo"))

    # static

    @staticmethod
    def uri() -> str:
        return "gs://bucket/file.txt"

    # private

    def __mock_web_detection_response(self) -> list:
        first_obj = mock.Mock()
        first_obj.entity_id = "a1"
        first_obj.score = 0.99
        first_obj.description = "desc"

        second_obj = mock.Mock()
        second_obj.entity_id = "a2"
        second_obj.score = 0.50
        second_obj.description = "desc2"

        return [first_obj, second_obj]

    def __mock_logo_detection_response(self) -> list:
        first_obj = mock.Mock()
        first_obj.entity_id = "l1"
        first_obj.score = 0.97
        first_obj.description = "desc"

        second_obj = mock.Mock()
        second_obj.entity_id = "l2"
        second_obj.score = 0.60
        second_obj.description = "desc2"

        return [first_obj, second_obj]
