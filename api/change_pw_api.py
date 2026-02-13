from api.base_api import BaseAPI


class ChangePasswordAPI(BaseAPI):
    ENDPOINT = "/api/profile"
    ALLOWED_FIELDS = {"name","phone", "address", "email", "password_old", "password"}

    def change_password(self, payload: dict):
        data = {}

        for k in self.ALLOWED_FIELDS:
            value = payload.get(k)
            if value in ("null", "", None):
                continue
            data[k] = value

        return self.patch(self.ENDPOINT, data=data)