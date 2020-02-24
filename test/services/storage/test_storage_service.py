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
    def test_that_raises_bucket_not_found_when_it_can_not_find_bucket(
        self, mock_retrieve: mock.MagicMock
    ):
        mock_retrieve.side_effect = StorageError.BucketNotFound

        with self.assertRaises(StorageError.BucketNotFound):
            self.service.set_bucket("abcde")
            self.service.request_retrieve(self.remote_file_path)

        mock_retrieve.assert_called_once_with(self.remote_file_path)

    @mock.patch.object(GCPProvider, "request_retrieve")
    def test_that_raises_file_not_found_when_it_can_not_find_object_in_storage(
        self, mock_retrieve: mock.MagicMock
    ):
        mock_retrieve.side_effect = StorageError.FileNotFound

        with self.assertRaises(StorageError.FileNotFound):
            self.service.set_bucket("bucket-testing")
            self.service.request_retrieve(self.remote_file_path)

        mock_retrieve.assert_called_once_with(self.remote_file_path)

    @mock.patch.object(GCPProvider, "request_retrieve")
    def test_that_can_request_retrieve(self, mock_response: mock.MagicMock):
        mock_response.return_value = self.__mock_existed_file_storage_response()

        self.service.set_bucket("bucket-testing")
        response = self.service.request_retrieve(self.remote_file_path)

        mock_response.assert_called_once_with(self.remote_file_path)

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("test.txt", response.get("name"))
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            response.get("public_url"),
        )
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertTrue(response.get("exists"))

    @mock.patch.object(GCPProvider, "request_upload")
    def test_that_can_request_upload(self, mock_response: mock.MagicMock):
        mock_response.return_value = self.__mock_existed_file_storage_response()

        self.service.set_bucket("bucket-testing")
        response = self.service.request_upload(
            self.remote_file_path, self.local_file_path
        )

        mock_response.assert_called_once_with(
            self.remote_file_path, self.local_file_path
        )

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("test.txt", response.get("name"))
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            response.get("public_url"),
        )
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertTrue(response.get("exists"))

    @mock.patch.object(GCPProvider, "request_delete")
    def test_that_can_request_delete(self, mock_response: mock.MagicMock):
        mock_response.return_value = self.__mock_deleted_file_storage_response()

        self.service.set_bucket("bucket-testing")
        response = self.service.request_delete(self.remote_file_path)

        mock_response.assert_called_once_with(self.remote_file_path)

        self.assertEqual(None, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("test.txt", response.get("name"))
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            response.get("public_url"),
        )
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertFalse(response.get("exists"))

    # static

    @staticmethod
    def bucket() -> object:
        class Bucket(object):
            name = "bucket-testing"

        return Bucket

    @staticmethod
    def remote_file_path() -> str:
        return "ex1/test.txt"

    @staticmethod
    def local_file_path() -> str:
        return "test.txt"

    # private

    def __mock_existed_file_storage_response(self) -> dict:
        return {
            "id": 1,
            "bucket": self.bucket().name,
            "name": "test.txt",
            "public_url": "https://storage.googleapis.com/{}/{}".format(
                self.bucket().name, self.remote_file_path()
            ),
            "uri": "gs://{}/{}".format(self.bucket().name, self.remote_file_path()),
            "exists": True,
        }

    def __mock_deleted_file_storage_response(self) -> dict:
        return {
            "id": None,
            "bucket": self.bucket().name,
            "name": "test.txt",
            "public_url": "https://storage.googleapis.com/{}/{}".format(
                self.bucket().name, self.remote_file_path()
            ),
            "uri": "gs://{}/{}".format(self.bucket().name, self.remote_file_path()),
            "exists": False,
        }
