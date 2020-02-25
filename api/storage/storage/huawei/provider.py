from api.storage.storage.base.provider import Provider as BaseProvider

from api.storage.storage.huawei.request import Request as HuaweiRequest

from obs import ObsClient


class Provider(BaseProvider):
    ACCESS_KEY = "ULECJ7LKRHVT7LSAO5QC"
    SECRET_KEY = "qgdMiJpHvI5BFChZxjQGsXFq7kWOaZBN91wfaZ6q"
    SERVER = "obs.ap-southeast-1.myhuaweicloud.com"

    def __init__(self):
        self.client = self.__set_client()

    def set_bucket(self, bucket: str) -> None:
        self.bucket = bucket

    def get_bucket(self) -> str:
        return self.bucket

    def request_retrieve(self, remote_file_path: str) -> dict:
        request = HuaweiRequest(self.client, self.bucket)
        retrieve_response = request.retrieve(remote_file_path)

        return retrieve_response

    # private

    def __set_client(self) -> ObsClient:
        return ObsClient(
            access_key_id=self.ACCESS_KEY,
            secret_access_key=self.SECRET_KEY,
            server=self.SERVER,
        )
