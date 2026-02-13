
class BaseAPI:
    def __init__(self, api_context):
        self.api_context = api_context

    def request(self, method, endpoint, data=None, params=None, headers=None):
        return self.api_context.fetch(
            endpoint,
            method=method,
            data=data,
            params=params,
            headers=headers
        )

    def get(self, endpoint, params=None, headers=None):
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint, data=None, headers=None):
        return self.request("POST", endpoint, data=data, headers=headers)

    def put(self, endpoint, data=None, headers=None):
        return self.request("PUT", endpoint, data=data, headers=headers)

    def patch(self, endpoint, data=None, headers=None):
        return self.request("PATCH", endpoint, data=data, headers=headers)

    def delete(self, endpoint, headers=None):
        return self.request("DELETE", endpoint, headers=headers)

