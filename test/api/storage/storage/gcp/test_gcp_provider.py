import unittest
import mock

from api.storage.storage.gcp.provider import Provider as GCPProvider
from api.storage.storage.gcp.request import Request as GCPRequest
from api.storage.storage.gcp.response import Response as GCPResponse

from lib.storage import errors as StorageError


class TestStorageStorageGCPProvider(unittest.TestCase):
    def setUp(self):
        self.provider = GCPProvider()

    def test_that_can_set_and_get_bucket(self):
        self.provider.set_bucket("bucket-testing")
        self.assertEqual("bucket-testing", self.provider.get_bucket())

    @mock.patch.object(GCPRequest, "upload")
    def test_that_raises_bucket_not_found_when_uploading_file_but_bucket_is_not_existed(
        self, mock_request: mock.MagicMock
    ):
        mock_request.side_effect = StorageError.BucketNotFound("")

        with self.assertRaises(StorageError.BucketNotFound):
            self.provider.set_bucket(self.bucket)
            self.provider.request_upload(self.remote_file_path, self.local_file_path)

        mock_request.assert_called_once_with(
            self.remote_file_path, self.local_file_path
        )

    @mock.patch.object(GCPRequest, "upload")
    def test_that_can_upload_file_to_bucket_and_parse_to_gcp_response(
        self, mock_request: mock.MagicMock
    ):
        mock_file_object = self.__mock_existed_file_object()

        mock_request.return_value = mock_file_object

        self.provider.set_bucket(self.bucket)
        response = self.provider.request_upload(
            self.remote_file_path, self.local_file_path
        )

        mock_request.assert_called_once_with(
            self.remote_file_path, self.local_file_path
        )

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertTrue(response.get("exists"))

    @mock.patch.object(GCPRequest, "delete")
    def test_that_raises_file_not_found_when_deleting_file_from_bucket_but_file_is_not_existed(
        self, mock_request: mock.MagicMock
    ):
        mock_request.side_effect = StorageError.FileNotFound("")

        with self.assertRaises(StorageError.FileNotFound):
            self.provider.set_bucket(self.bucket)
            self.provider.request_delete(self.remote_file_path)

        mock_request.assert_called_once_with(self.remote_file_path)

    @mock.patch.object(GCPRequest, "delete")
    def test_that_can_delete_file_from_bucket_and_parse_to_gcp_response(
        self, mock_request: mock.MagicMock
    ):
        mock_file_object = self.__mock_deleted_file_object()

        mock_request.return_value = mock_file_object

        self.provider.set_bucket(self.bucket)
        response = self.provider.request_delete(self.remote_file_path)

        mock_request.assert_called_once_with(self.remote_file_path)

        self.assertEqual(None, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertFalse(response.get("exists"))

    @mock.patch.object(GCPRequest, "retrieve")
    def test_that_raises_file_not_found_when_retrieving_file_from_bucket_but_file_is_not_existed(
        self, mock_request: mock.MagicMock
    ):
        mock_request.side_effect = StorageError.FileNotFound("")

        with self.assertRaises(StorageError.FileNotFound):
            self.provider.set_bucket(self.bucket)
            self.provider.request_retrieve(self.remote_file_path)

        mock_request.assert_called_once_with(self.remote_file_path)

    @mock.patch.object(GCPRequest, "retrieve")
    def test_that_can_retrieve_file_from_bucket(self, mock_request: mock.MagicMock):
        mock_file_object = self.__mock_existed_file_object()

        mock_request.return_value = mock_file_object

        self.provider.set_bucket(self.bucket)
        response = self.provider.request_retrieve(self.remote_file_path)

        mock_request.assert_called_once_with(self.remote_file_path)

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertTrue(response.get("exists"))

    # static

    @staticmethod
    def bucket():
        class Bucket(object):
            name = "bucket-testing"

        return Bucket

    @staticmethod
    def remote_file_path():
        return "ex1/test.txt"

    @staticmethod
    def local_file_path():
        return "test.txt"

    # private

    def __mock_existed_file_object(self):
        obj = mock.Mock()
        obj.id = 1
        obj.bucket = self.bucket()
        obj.name = self.remote_file_path()
        obj.public_url = "https://storage.googleapis.com/{}/{}".format(
            self.bucket(), self.remote_file_path()
        )
        obj.exists = lambda: True

        return obj

    def __mock_deleted_file_object(self):
        obj = mock.Mock()
        obj.id = None
        obj.bucket = self.bucket()
        obj.name = self.remote_file_path()
        obj.public_url = "https://storage.googleapis.com/{}/{}".format(
            self.bucket(), self.remote_file_path()
        )
        obj.exists = lambda: False

        return obj
