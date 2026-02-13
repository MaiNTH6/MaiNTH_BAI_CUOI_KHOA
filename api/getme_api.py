# api/getme_api.py
from api.base_api import BaseAPI
class GetMeAPI(BaseAPI):
    ENDPOINT = "/api/me"

    def get_me(self):
        return self.get(self.ENDPOINT)