# components/api/profile_api.py
from api.base_api import BaseAPI
class ProfileAPI(BaseAPI):
    ENDPOINT = "/api/profile"
    # ENDPOINT_AVATAR = "/api/file"
    ALLOWED_FIELDS = {"name", "phone", "address"}

    def update_profile(self, data: dict):
        payload = {}

        for k in self.ALLOWED_FIELDS:
            value = data.get(k)
            if value in ("null", "", None):
                continue
            payload[k] = value

        return self.patch(self.ENDPOINT, data=payload)
    