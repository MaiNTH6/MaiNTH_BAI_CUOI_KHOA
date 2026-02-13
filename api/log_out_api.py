from api.base_api import BaseAPI
class LogOutAPI(BaseAPI):
    ENDPOINT = "/api/logout"

    def log_out(self):
        return self.delete(self.ENDPOINT)