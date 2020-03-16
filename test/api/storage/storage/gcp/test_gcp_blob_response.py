import unittest
import mock

from api.storage.storage.gcp.blob_response import BlobResponse


class TestStorageStorageGCPBlobResponse(unittest.TestCase):
    def setUp(self):
        self.response = BlobResponse(self.__mock_blob_object())

    def test_that_returns_id_as_integer(self):
        self.assertEqual(1, self.response.id())

    def test_that_returns_bucket_as_string(self):
        self.assertEqual("bucket-testing", self.response.bucket())

    def test_that_returns_file_name_as_string(self):
        self.assertEqual("ex1/test.txt", self.response.name())

    def test_that_returns_file_public_url_as_string(self):
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            self.response.public_url(),
        )

    def test_that_returns_file_uri_as_string(self):
        self.assertEqual("gs://bucket-testing/ex1/test.txt", self.response.uri())

    def test_that_returns_file_exists_true_if_file_is_existed(self):
        self.assertTrue(self.response.exists())

    def test_that_returns_file_exists_false_if_file_is_not_existed(self):
        response = BlobResponse(self.__mock_deleted_blob_object())

        self.assertFalse(response.exists())

    def test_that_can_serialize_to_dict(self):
        serialize = self.response.serialize()

        self.assertEqual(1, serialize.get("id"))
        self.assertEqual("bucket-testing", serialize.get("bucket"))
        self.assertEqual("ex1/test.txt", serialize.get("name"))
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            serialize.get("public_url"),
        )
        self.assertEqual("gs://bucket-testing/ex1/test.txt", serialize.get("uri"))
        self.assertTrue(serialize.get("exists"))

    # static

    @staticmethod
    def bucket() -> object:
        class Bucket(object):
            name = "bucket-testing"

        return Bucket

    @staticmethod
    def remote_file_path() -> str:
        return "ex1/test.txt"

    # private

    def __mock_blob_object(self) -> object:
        blob = mock.Mock()
        blob.object.id = 1
        blob.object.bucket = self.bucket()
        blob.object.name = self.remote_file_path()
        blob.object.public_url = "https://storage.googleapis.com/{}/{}".format(
            self.bucket().name, self.remote_file_path()
        )
        blob.object.exists = lambda: True

        return blob

    def __mock_deleted_blob_object(self) -> object:
        blob = mock.Mock()
        blob.object.id = None
        blob.object.bucket = self.bucket()
        blob.object.name = self.remote_file_path()
        blob.object.public_url = "https://storage.googleapis.com/{}/{}".format(
            self.bucket().name, self.remote_file_path()
        )
        blob.object.exists = lambda: False

        return blob
