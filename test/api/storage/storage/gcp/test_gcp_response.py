import unittest
import mock

from api.storage.storage.gcp.response import Response as GCPResponse


class TestGCPResponse(unittest.TestCase):
    def setUp(self):
        self.response = GCPResponse(self.__mock_existing_file_object())

    def test_that_returns_id_as_integer(self):
        self.assertEqual(1, self.response.id())

    def test_that_returns_bucket_as_string(self):
        self.assertEqual("bucket-testing", self.response.bucket())

    def test_that_returns_file_name_as_string(self):
        self.assertEqual("test.txt", self.response.name())

    def test_that_returns_file_public_url_as_string(self):
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            self.response.public_url(),
        )

    def test_that_returns_file_exists_true_if_file_is_existed(self):
        self.assertTrue(self.response.exists())

    def test_that_returns_file_existing_false_if_file_is_not_existed(self):
        file_obj = self.__mock_existing_file_object()
        file_obj.exists = lambda: False

        response = GCPResponse(file_obj)

        self.assertFalse(response.exists())

    # static

    @staticmethod
    def bucket():
        return "bucket-testing"

    @staticmethod
    def remote_file_path():
        return "ex1/test.txt"

    @staticmethod
    def local_file_path():
        return "test.txt"

    # private

    def __mock_existing_file_object(self):
        obj = mock.Mock()
        obj.id = 1
        obj.bucket = self.bucket()
        obj.name = self.local_file_path()
        obj.public_url = "https://storage.googleapis.com/{}/{}".format(
            self.bucket(), self.remote_file_path()
        )
        obj.exists = lambda: True

        return obj
