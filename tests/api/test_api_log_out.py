import pytest
import allure
from api.log_out_api import LogOutAPI
from utils.api_assertions import assert_status_code
@allure.epic("API")
@allure.feature("Auth")
@allure.story("Log Out")
def test_log_out_success(api_context_authenticated):
    log_out_api = LogOutAPI(api_context_authenticated)
    response = log_out_api.log_out()

    assert_status_code(response, 200)