from api.timer_api import APITimer
from api.reporter_api import APIReporter

def execute_api(
    api_call,
    payload=None,
    *,
    endpoint: str,
    method: str = "POST",
    attach: bool = True,
    **kwargs
):
    """
    Generic API executor

    :param api_call: callable API method (e.g. login_api.login)
    :param payload: request payload
    :param endpoint: API endpoint (for report only)
    :param method: HTTP method
    :param attach: attach to Allure or not
    :param file_path: path to file to upload (if any)
    :return: (response, response_time)
    """

    response, response_time = APITimer.measure(api_call, payload, **kwargs)

    if attach:
        APIReporter.attach_api_info(
            method=method,
            endpoint=endpoint,
            payload=payload,
            response=response,
            response_time=response_time,
            request_data=kwargs
        )

    return response, response_time
