import unittest
import mock

from google.cloud import exceptions

from api.storage.storage.gcp.request import Request as GCPRequest

from lib.storage import errors as StorageError


class TestStorageStorageGCPRequest(unittest.TestCase):
    def setUp(self):
        self.request = GCPRequest("abcde")

    @mock.patch.object(GCPRequest, "_Request__storage_client")
    def test_that_raises_error_when_it_can_not_find_bucket(self, mock_storage_client):
        mock_storage_client.side_effect = exceptions.NotFound("")

        with self.assertRaises(StorageError.BucketNotFound):
            self.request.upload(self.remote_file_path, self.local_file_path)

        mock_storage_client.assert_called_once()

    @mock.patch.object(GCPRequest, "_Request__blob_object")
    @mock.patch.object(GCPRequest, "_Request__upload_to_storage")
    def test_that_can_upload_file_to_gcp_bucket(self, mock_upload, mock_blob):
        mock_blob_object = self.__mock_blob_object()
        mock_file_object = self.__mock_existing_file_object()

        mock_blob.return_value = mock_blob_object
        mock_upload.return_value = mock_file_object

        response = self.request.upload(self.remote_file_path, self.local_file_path)

        mock_blob.assert_called_once_with(self.remote_file_path)
        mock_upload.assert_called_once_with(mock_blob_object, self.local_file_path)

        self.assertEqual(1, response.id)
        self.assertEqual("bucket-testing", response.bucket)
        self.assertTrue(response.exists())

    @mock.patch.object(GCPRequest, "_Request__blob_object")
    def test_that_can_not_delete_file_from_gcp_bucket_when_file_is_not_existed(
        self, mock_blob
    ):
        mock_blob.return_value = self.__mock_deleting_file_object()

        with self.assertRaises(StorageError.FileNotFound):
            self.request.delete(self.remote_file_path)

        mock_blob.assert_called_once()

    @mock.patch.object(GCPRequest, "_Request__blob_object")
    @mock.patch.object(GCPRequest, "_Request__delete_from_storage")
    def test_that_can_delete_file_from_gcp_bucket(self, mock_delete, mock_blob):
        mock_blob_object = self.__mock_blob_object()
        mock_file_object = self.__mock_deleting_file_object()

        mock_blob.return_value = mock_blob_object
        mock_delete.return_value = mock_file_object

        response = self.request.delete(self.remote_file_path)

        mock_blob.assert_called_once_with(self.remote_file_path)
        mock_delete.assert_called_once()

        self.assertEqual(None, response.id)
        self.assertEqual("bucket-testing", response.bucket)
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

    def __mock_blob_object(self):
        obj = mock.Mock()
        obj.upload_from_filename = lambda local_file_path: "uploading"
        obj.delete = lambda: "deleting"

        return obj

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
