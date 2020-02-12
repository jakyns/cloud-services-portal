import unittest
import mock

from api.storage.storage.gcp.provider import Provider as GCPProvider
from api.storage.storage.gcp.request import Request as GCPRequest
from api.storage.storage.gcp.response import Response as GCPResponse

from lib.storage import errors as StorageError


class TestStorageStorageGCPProvider(unittest.TestCase):
    def setUp(self):
        self.provider = GCPProvider()

    def test_that_can_set_bucket(self):
        self.provider.set_bucket(self.bucket)

        assert self.bucket == self.provider.bucket

    @mock.patch.object(GCPRequest, "upload")
    def test_that_raises_bucket_not_found_when_bucket_is_not_existed(
        self, mock_request
    ):
        mock_request.side_effect = StorageError.BucketNotFound("")

        with self.assertRaises(StorageError.BucketNotFound):
            self.provider.set_bucket(self.bucket)
            self.provider.request_upload(self.remote_file_path, self.local_file_path)

        mock_request.assert_called_once()

    @mock.patch.object(GCPRequest, "upload")
    @mock.patch.object(GCPProvider, "_Provider__build_storage_response")
    def test_that_can_upload_file_to_gcp_bucket_and_parse_to_gcp_response(
        self, mock_response, mock_request
    ):
        mock_file_object = self.__mock_existing_file_object()

        mock_request.return_value = mock_file_object
        mock_response.return_value = GCPResponse(mock_file_object)

        self.provider.set_bucket(self.bucket)
        response = self.provider.request_upload(
            self.remote_file_path, self.local_file_path
        )

        mock_request.assert_called_once_with(
            self.remote_file_path, self.local_file_path
        )
        mock_response.assert_called_once_with(mock_file_object)

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertTrue(response.get("exists"))

    @mock.patch.object(GCPRequest, "delete")
    def test_that_raises_file_not_found_when_file_from_gcp_bucket_is_not_existed(
        self, mock_request
    ):
        mock_request.side_effect = StorageError.FileNotFound("")

        with self.assertRaises(StorageError.FileNotFound):
            self.provider.set_bucket(self.bucket)
            self.provider.request_delete(self.remote_file_path)

        mock_request.assert_called_once()

    @mock.patch.object(GCPRequest, "delete")
    @mock.patch.object(GCPProvider, "_Provider__build_storage_response")
    def test_that_can_delete_file_from_gcp_bucket_and_parse_to_gcp_response(
        self, mock_response, mock_request
    ):
        mock_file_object = self.__mock_deleting_file_object()

        mock_request.return_value = mock_file_object
        mock_response.return_value = GCPResponse(mock_file_object)

        self.provider.set_bucket(self.bucket)
        response = self.provider.request_delete(self.remote_file_path)

        mock_request.assert_called_once_with(self.remote_file_path)
        mock_response.assert_called_once_with(mock_file_object)

        self.assertEqual(None, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertFalse(response.get("exists"))

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

    def __mock_deleting_file_object(self):
        obj = mock.Mock()
        obj.id = None
        obj.bucket = self.bucket()
        obj.name = self.local_file_path()
        obj.public_url = "https://storage.googleapis.com/{}/{}".format(
            self.bucket(), self.remote_file_path()
        )
        obj.exists = lambda: False

        return obj
