import pytest
import allure


from api.login_api import LoginAPI
from api.timer_api import APITimer
from api.reporter_api import APIReporter
from utils.excel_reader import read_excel
from utils.api_assertions import assert_login_response
from utils.api_test_executor import execute_api


# ========= Reader data =========
TEST_DATA = read_excel("data/user_login.xlsx", sheet_name="Sheet1")

@allure.epic("API")
@allure.feature("Auth")
@allure.story("Login")
@pytest.mark.parametrize("data", TEST_DATA)
def test_login_user(api_context, data):
    login_api = LoginAPI(api_context)

    response, response_time = execute_api(
        login_api.login_user,
        payload=data,
        endpoint=login_api.ENDPOINT,
        method="POST",
        attach=True
    )
    assert_login_response(
        response, 
        data
        )
    assert response_time <= data.get("max_response_time"), f"Response time {response_time}s > {data.get('max_response_time')}s"
