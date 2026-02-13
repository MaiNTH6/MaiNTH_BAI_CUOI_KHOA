# api/login_api.py
from api.base_api import BaseAPI
class LoginAPI(BaseAPI):
    ENDPOINT = "/api/login"

    def login_user(self, payload):
        return self.post(self.ENDPOINT, data=payload)

