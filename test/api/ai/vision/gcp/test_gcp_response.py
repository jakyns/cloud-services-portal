import unittest
import mock

from api.ai.vision.gcp.response import Response as GCPResponse


class TestStorageStorageGCPResponse(unittest.TestCase):
    def test_that_can_serialize_web_detection_response(self):
        response_obj = GCPResponse(self.__mock_web_detection_response())
        response = response_obj.web_detection_serialize()

        self.assertEqual(0.99, response[0].get("score"))
        self.assertEqual("desc", response[0].get("label"))
        self.assertEqual(0.50, response[1].get("score"))
        self.assertEqual("desc2", response[1].get("label"))

    def test_that_can_serialize_logo_detection_response(self):
        response_obj = GCPResponse(self.__mock_logo_detection_response())
        response = response_obj.logo_detection_serialize()

        self.assertEqual(0.97, response[0].get("score"))
        self.assertEqual("desc", response[0].get("logo"))
        self.assertEqual(0.60, response[1].get("score"))
        self.assertEqual("desc2", response[1].get("logo"))

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
