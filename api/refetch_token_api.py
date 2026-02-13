# test api curl https://book.anhtester.com/api/refetch-token \
#   --request POST \
#   --cookie 'refetchToken='
# components/api/refetch_token_api.py
from api.base_api import BaseAPI
class RefetchTokenAPI(BaseAPI):
    ENDPOINT = "/api/refetch-token"

    def refetch_token(self):
        return self.post(self.ENDPOINT)