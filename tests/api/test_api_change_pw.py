import pytest
import allure

from api.change_pw_api import ChangePasswordAPI
from utils.api_assertions import ( 
    assert_status_code,
    assert_change_password_response    
)
from utils.api_test_executor import execute_api
from utils.excel_reader import read_excel

TEST_DATA_CHANGE_PW = read_excel(
    "data/change_pw.xlsx", sheet_name="Sheet1"
)

@allure.epic("API")
@allure.feature("User")
@allure.story("Change Password")
@pytest.mark.parametrize("data", TEST_DATA_CHANGE_PW)

def test_change_password(api_context_change_pw, data):
    change_pw_api = ChangePasswordAPI(api_context_change_pw)

    response, response_time = execute_api(
        change_pw_api.change_password,
        payload=data,
        endpoint=change_pw_api.ENDPOINT,
        method="PATCH"
    )

    expected_status = data.get("expected_status", 200)
    assert_status_code(response, expected_status)

    body = response.json()

    if expected_status == 200:
        assert "msg" in body
    else:
        assert "msg" in body or "fields" in body
   
    assert response_time <= data.get("max_response_time"), f"Response time {response_time}s > {data.get('max_response_time')}s"