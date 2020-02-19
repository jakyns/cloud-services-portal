import unittest
import mock

from lib.storage import errors as StorageError

from api.storage.storage.gcp.provider import Provider as GCPProvider

from services.storage import StorageService


class TestServiceStorageService(unittest.TestCase):
    def setUp(self):
        self.service = StorageService("GCP")

    def test_that_raises_error_when_initialize_provider_which_is_not_available(self):
        with self.assertRaises(StorageError.ProviderNotFound):
            StorageService("abcde")

    def test_that_can_initiate_provider(self):
        self.assertIsInstance(self.service, StorageService)
        self.assertIsInstance(self.service.provider, GCPProvider)

    def test_that_can_set_and_get_bucket(self):
        self.service.set_bucket("bucket-testing")
        self.assertEqual("bucket-testing", self.service.get_bucket())

        self.service.set_bucket("bucket-testing2")
        self.assertEqual("bucket-testing2", self.service.get_bucket())

    @mock.patch.object(GCPProvider, "request_retrieve")
    def test_that_can_request_retrieve(self, mock_upload):
        mock_upload.return_value = self.__mock_file_object()

        self.service.request_retrieve(self.remote_file_path)

        mock_upload.assert_called_once_with(self.remote_file_path)

    @mock.patch.object(GCPProvider, "request_upload")
    def test_that_can_request_upload(self, mock_upload):
        mock_upload.return_value = self.__mock_file_object()

        self.service.request_upload(self.remote_file_path, self.local_file_path)

        mock_upload.assert_called_once_with(self.remote_file_path, self.local_file_path)

    @mock.patch.object(GCPProvider, "request_delete")
    def test_that_can_request_delete(self, mock_delete):
        mock_delete.return_value = self.__mock_file_object()

        self.service.request_delete(self.remote_file_path)

        mock_delete.assert_called_once_with(self.remote_file_path)

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

    def __mock_file_object(self):
        obj = mock.Mock()
        obj.id = 1
        obj.bucket = self.bucket()
        obj.name = self.local_file_path()
        obj.public_url = "https://storage.googleapis.com/{}/{}".format(
            self.bucket(), self.remote_file_path()
        )
        obj.exists = lambda: True

        return obj
