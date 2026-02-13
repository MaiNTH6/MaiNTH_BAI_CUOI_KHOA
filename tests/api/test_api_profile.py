import  pytest
import  allure
from api import upload_api
from api.profile_api import ProfileAPI

from utils.api_assertions import (
    assert_status_code,
    assert_profile_data
)
from utils.api_test_executor import execute_api
from utils.excel_reader import read_excel


TEST_DATA_PROFILE = read_excel(
    "data/user_profile.xlsx",sheet_name="Sheet1"
)
@allure.epic("API")
@allure.feature("User")
@allure.story("Profile")
@pytest.mark.parametrize("data", TEST_DATA_PROFILE)
def test_update_profile(api_context_authenticated, data):
    profile_api = ProfileAPI(api_context_authenticated)

    response, response_time = execute_api(
        profile_api.update_profile,
        payload=data,
        endpoint=profile_api.ENDPOINT,
        attach=True
    )
    expected_status = data.get("expected_status") or 200    
    assert_status_code(response, expected_status)
    body = response.json()
    assert_profile_data(body, data)
    assert response_time <= data.get("max_response_time"), f"Response time {response_time}s > {data.get('max_response_time')}s"
