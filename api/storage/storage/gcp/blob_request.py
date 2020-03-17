from google.cloud import storage
from google.cloud import exceptions

from lib.storage import errors as StorageError


class BlobRequest(object):
    def __init__(self, bucket: storage.bucket.Bucket, remote_file_path: str):
        self.blob = bucket.blob(remote_file_path)

    def upload(self, local_file_path: str) -> bool:
        try:
            self.blob.upload_from_filename(local_file_path)
            return True
        except FileNotFoundError:
            raise StorageError.FileNotFound("uploading file not found")

    def delete(self) -> bool:
        try:
            self.blob.delete()
            return True
        except exceptions.NotFound:
            raise StorageError.FileNotFound("Can not delete, object file not found")

    def is_existed(self) -> bool:
        if not self.blob.exists():
            raise StorageError.FileNotFound(
                f"{self.object.name} object is not existed in GCP storage"
            )

        return True
