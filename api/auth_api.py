
from api.base_api import BaseAPI
class AuthAPI(BaseAPI):
    def login(self, payload: dict):
        return self.post(
            "/api/login",
            data={
                "email": payload.get("email", ""),
                "password": payload.get("password", "")
            }
        )
    def login_get_token(self, email, password):
        response = self.login({
            "email": email,
            "password": password
        })
        assert response.status == 200, f"Login failed: {response.text()}"
        return response.json().get("accessToken")
