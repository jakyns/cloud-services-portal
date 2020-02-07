import unittest
import mock

from google.cloud import exceptions

from api.storage.storage.gcp.provider import Provider as GCPProvider
from api.storage.storage.gcp.response import Response as GCPResponse

from lib.storage import errors as StorageError


class TestGCPProvider(unittest.TestCase):
    def setUp(self):
        self.provider = GCPProvider()

    def test_that_can_set_bucket(self):
        self.provider.set_bucket(self.bucket)

        assert self.bucket == self.provider.bucket

    @mock.patch.object(GCPProvider, "_Provider__storage_client")
    def test_that_raises_error_when_it_can_not_find_bucket(self, mock_storage_client):
        mock_storage_client.side_effect = exceptions.NotFound("")

        with self.assertRaises(StorageError.BucketNotFound):
            self.provider.set_bucket(self.bucket)
            self.provider.request_upload(self.remote_file_path, self.local_file_path)

        mock_storage_client.assert_called_once()

    @mock.patch.object(GCPProvider, "_Provider__upload")
    @mock.patch.object(GCPProvider, "_Provider__build_storage_response")
    def test_that_can_upload_file_to_gcp_bucket(self, mock_response, mock_upload):
        mock_file_object = self.__mock_existing_file_object()

        mock_upload.return_value = mock_file_object
        mock_response.return_value = GCPResponse(mock_file_object)

        self.provider.set_bucket(self.bucket)
        response = self.provider.request_upload(
            self.remote_file_path, self.local_file_path
        )

        mock_upload.assert_called_once_with(self.remote_file_path, self.local_file_path)
        mock_response.assert_called_once_with(mock_file_object)

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertTrue(response.get("exists"))

    @mock.patch.object(GCPProvider, "_Provider__blob_object")
    def test_that_can_not_delete_file_from_gcp_bucket_when_file_is_not_existed(
        self, mock_blob
    ):
        mock_blob.return_value = self.__mock_deleting_file_object()

        with self.assertRaises(StorageError.FileNotFound):
            self.provider.set_bucket(self.bucket)
            self.provider.request_delete(self.remote_file_path)

        mock_blob.assert_called_once()

    @mock.patch.object(GCPProvider, "_Provider__delete")
    @mock.patch.object(GCPProvider, "_Provider__build_storage_response")
    def test_that_can_delete_file_from_gcp_bucket(self, mock_response, mock_upload):
        mock_file_object = self.__mock_deleting_file_object()

        mock_upload.return_value = mock_file_object
        mock_response.return_value = GCPResponse(mock_file_object)

        self.provider.set_bucket(self.bucket)
        response = self.provider.request_delete(self.remote_file_path)

        mock_upload.assert_called_once_with(self.remote_file_path)
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
