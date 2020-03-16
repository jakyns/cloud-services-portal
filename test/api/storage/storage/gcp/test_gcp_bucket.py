import unittest
import mock

from google.cloud import storage
from google.cloud import exceptions

from lib.storage import errors as StorageError

from api.storage.storage.gcp.bucket import Bucket
from api.storage.storage.gcp.blob_request import BlobRequest
from api.storage.storage.gcp.blob_response import BlobResponse


class StorageClientTesting(object):
    def get_bucket(self, bucket) -> storage.bucket.Bucket:
        return BucketTesting()


class BucketTesting(object):
    def blob(self, remote_file_path) -> storage.blob.Blob:
        return storage.blob.Blob


class TestStorageStorageGCPBucket(unittest.TestCase):
    @mock.patch.object(storage.client.Client, "get_bucket")
    def test_that_raises_bucket_not_found_when_it_can_not_find_bucket(
        self, mock_bucket: mock.MagicMock
    ):
        mock_bucket.side_effect = exceptions.NotFound("")

        with self.assertRaises(StorageError.BucketNotFound):
            Bucket(storage.Client(), self.bucket().name)

        mock_bucket.assert_called_once_with(self.bucket().name)

    def test_that_can_return_bucket_name(self):
        bucket = Bucket(StorageClientTesting(), self.bucket().name)

        self.assertEqual("bucket-testing", bucket.name())

    @mock.patch.object(BlobRequest, "is_existed")
    def test_that_raises_file_not_found_when_it_can_not_retrieve_file(
        self, mock_blob: mock.MagicMock
    ):
        mock_blob.side_effect = StorageError.FileNotFound

        with self.assertRaises(StorageError.FileNotFound):
            bucket = Bucket(StorageClientTesting(), self.bucket().name)
            bucket.retrieve(self.remote_file_path)

        mock_blob.assert_called_once()

    @mock.patch.object(BlobRequest, "is_existed")
    @mock.patch.object(BlobResponse, "serialize")
    def test_that_returns_file_properties_when_file_is_existed_in_bucket(
        self, mock_blob_response: mock.MagicMock, mock_blob: mock.MagicMock
    ):
        mock_blob.return_value = True
        mock_blob_response.return_value = self.__mock_existed_blob_response()

        bucket = Bucket(StorageClientTesting(), self.bucket())
        response = bucket.retrieve(self.remote_file_path)

        mock_blob.assert_called_once()
        mock_blob_response.assert_called_once()

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("ex1/test.txt", response.get("name"))
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            response.get("public_url"),
        )
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertTrue(response.get("exists"))

    @mock.patch.object(BlobRequest, "upload")
    def test_that_raises_file_not_found_when_local_file_is_not_existed(
        self, mock_blob: mock.MagicMock
    ):
        mock_blob.side_effect = StorageError.FileNotFound

        with self.assertRaises(StorageError.FileNotFound):
            bucket = Bucket(StorageClientTesting(), self.bucket())
            bucket.upload(self.remote_file_path, self.local_file_path)

        mock_blob.assert_called_once_with(self.local_file_path)

    @mock.patch.object(BlobRequest, "upload")
    @mock.patch.object(BlobResponse, "serialize")
    def test_that_returns_uploaded_file_properties_when_uploading_file_succeed(
        self, mock_blob_response: mock.MagicMock, mock_blob: mock.MagicMock
    ):
        mock_blob.return_value = True
        mock_blob_response.return_value = self.__mock_existed_blob_response()

        bucket = Bucket(StorageClientTesting(), self.bucket())
        response = bucket.upload(self.remote_file_path, self.local_file_path)

        mock_blob.assert_called_once()
        mock_blob_response.assert_called_once()

        self.assertEqual(1, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("ex1/test.txt", response.get("name"))
        self.assertEqual(
            "https://storage.googleapis.com/bucket-testing/ex1/test.txt",
            response.get("public_url"),
        )
        self.assertEqual("gs://bucket-testing/ex1/test.txt", response.get("uri"))
        self.assertTrue(response.get("exists"))

    @mock.patch.object(BlobRequest, "is_existed")
    def test_that_raises_file_not_found_when_it_can_not_delete_file_in_storage(
        self, mock_blob: mock.MagicMock
    ):
        mock_blob.side_effect = StorageError.FileNotFound

        with self.assertRaises(StorageError.FileNotFound):
            bucket = Bucket(StorageClientTesting(), self.bucket())
            bucket.delete(self.remote_file_path)

        mock_blob.assert_called_once()

    @mock.patch.object(BlobRequest, "is_existed")
    @mock.patch.object(BlobRequest, "delete")
    @mock.patch.object(BlobResponse, "serialize")
    def test_that_returns_deleted_file_properties_when_it_can_delete_file_from_storage(
        self,
        mock_blob_response: mock.MagicMock,
        mock_deleted_blob: mock.MagicMock,
        mock_blob: mock.MagicMock,
    ):
        mock_blob.return_value = True
        mock_deleted_blob.return_value = True
        mock_blob_response.return_value = self.__mock_deleted_blob_response()

        bucket = Bucket(StorageClientTesting(), self.bucket())
        response = bucket.delete(self.remote_file_path)

        mock_blob.assert_called_once()
        mock_deleted_blob.assert_called_once()
        mock_blob_response.assert_called_once()

        self.assertEqual(None, response.get("id"))
        self.assertEqual("bucket-testing", response.get("bucket"))
        self.assertEqual("ex1/test.txt", response.get("name"))
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
    def local_file_path() -> str:
        return "test.txt"

    @staticmethod
    def remote_file_path() -> str:
        return "ex1/test.txt"

    # private

    def __mock_existed_blob_response(self) -> dict:
        return {
            "id": 1,
            "bucket": self.bucket().name,
            "name": self.remote_file_path(),
            "public_url": f"https://storage.googleapis.com/{self.bucket().name}/{self.remote_file_path()}",
            "uri": f"gs://{self.bucket().name}/{self.remote_file_path()}",
            "exists": True,
        }

    def __mock_deleted_blob_response(self) -> dict:
        return {
            "id": None,
            "bucket": self.bucket().name,
            "name": self.remote_file_path(),
            "public_url": f"https://storage.googleapis.com/{self.bucket().name}/{self.remote_file_path()}",
            "uri": f"gs://{self.bucket().name}/{self.remote_file_path()}",
            "exists": False,
        }
