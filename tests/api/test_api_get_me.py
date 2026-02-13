from urllib import response
import  pytest
import  allure
from api.getme_api import GetMeAPI
from utils.api_assertions import (
    assert_status_code,
    assert_me_response
)
from utils.api_test_executor import execute_api


@allure.epic("API")
@allure.feature("User")
@allure.story("Get Me")
def test_get_me_success(api_context_authenticated):
    getme_api = GetMeAPI(api_context_authenticated)

    response, response_time = execute_api(
        getme_api.get_me,
        endpoint=getme_api.ENDPOINT,
        method="GET",
        attach=True
    )

    assert_me_response(response)
    assert response_time <= 2, f"Response time {response_time}s > 2s"



def test_get_me_unauthorized(api_context):
    getme_api = GetMeAPI(api_context)

    response, response_time = execute_api(
        api_call=getme_api.get_me,
        endpoint=getme_api.ENDPOINT,
        method="GET",
        attach=True
    )

    # ===== Assertions =====
    assert_status_code(response, 401)

    body = response.json()
    assert body.get("msg") == "Missing or invalid Authorization header"
