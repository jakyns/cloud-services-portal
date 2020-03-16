import unittest
import mock

from google.cloud import storage
from google.cloud import exceptions

from lib.storage import errors as StorageError

from api.storage.storage.gcp.blob_request import BlobRequest


class BucketTesting(object):
    def blob(self, remote_file_path) -> storage.blob.Blob:
        return storage.blob.Blob


class TestStorageStorageGCPBlobRequest(unittest.TestCase):
    def setUp(self):
        self.blob = BlobRequest(BucketTesting(), self.remote_file_path())

    @mock.patch.object(storage.blob.Blob, "upload_from_filename")
    def test_that_raises_uploading_file_not_found_when_local_file_is_not_existed(
        self, mock_object: mock.MagicMock
    ):
        mock_object.side_effect = FileNotFoundError

        with self.assertRaises(StorageError.FileNotFound):
            self.blob.upload(self.local_file_path)

        mock_object.assert_called_once_with(self.local_file_path)

    @mock.patch.object(storage.blob.Blob, "upload_from_filename")
    def test_that_returns_true_when_it_can_upload_file(
        self, mock_object: mock.MagicMock
    ):
        mock_object.return_value = True

        response = self.blob.upload(self.local_file_path)

        mock_object.assert_called_once_with(self.local_file_path)

        self.assertTrue(response)

    @mock.patch.object(storage.blob.Blob, "delete")
    def test_that_raises_can_not_delete_when_file_is_not_existed(
        self, mock_object: mock.MagicMock
    ):
        mock_object.side_effect = exceptions.NotFound("")

        with self.assertRaises(StorageError.FileNotFound):
            self.blob.delete(self.remote_file_path)

        mock_object.assert_called_once()

    @mock.patch.object(storage.blob.Blob, "delete")
    def test_that_returns_true_when_it_can_delete_file(
        self, mock_object: mock.MagicMock
    ):
        mock_object.return_value = True

        response = self.blob.delete(self.remote_file_path)

        mock_object.assert_called_once()

        self.assertTrue(response)

    @mock.patch.object(storage.blob.Blob, "exists")
    def test_that_raises_error_file_not_found_when_blob_object_is_not_existed(
        self, mock_object: mock.MagicMock
    ):
        mock_object.side_effect = StorageError.FileNotFound

        with self.assertRaises(StorageError.FileNotFound):
            self.blob.is_existed()

        mock_object.assert_called_once()

    @mock.patch.object(storage.blob.Blob, "exists")
    def test_that_returns_true_when_blob_is_existed(self, mock_object: mock.MagicMock):
        mock_object.return_value = True

        response = self.blob.is_existed()

        mock_object.assert_called_once()

        self.assertTrue(response)

    # static

    @staticmethod
    def remote_file_path() -> str:
        return "ex1/test.txt"

    @staticmethod
    def local_file_path() -> str:
        return "test.txt"
