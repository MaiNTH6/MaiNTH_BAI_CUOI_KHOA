# tests/ui/test_update_profile.py

import pytest
import allure

import data
from pages.profile_page import ProfilePage
from components.menu_profile import MenuProfile
from utils.excel_reader import read_excel
from api.getme_api import GetMeAPI
from utils.api_test_executor import execute_api
from utils.verify_helpers import verify_field
from utils.api_assertions import assert_status_code


TEST_DATA = read_excel("data/profile_ui_data.xlsx", "Sheet1")


@allure.epic("UI")
@allure.feature("User")
@allure.story("Update Profile")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("data", TEST_DATA)
def test_update_profile(login, api_context_authenticated, data):
    """
    Test flow:
    1. Login
    2. Navigate to Profile page
    3. Update profile via UI
    4. Verify success message
    5. Call API GET /me to verify updated data
    """

    page = login
    profile_page = ProfilePage(page)

    # Step 1: Navigate to Profile
    with allure.step("Open Profile page from avatar menu"):
        MenuProfile(page).open_profile()

    # Step 2: Update profile
    with allure.step("Fill profile form"):
        profile_page.fill_profile(data)

    with allure.step("Click save profile"):
        profile_page.save_profile()

    # Step 3: Verify success message
    with allure.step("Verify update success message"):
        profile_page.verify_update_success(data.get("expected_message"))

    # Step 4: Verify data with API
    # ===== API GET /me =====
    getme_api = GetMeAPI(api_context_authenticated)

    response_get, _ = execute_api(
        getme_api.get_me,
        endpoint=getme_api.ENDPOINT,
        attach=True
    )
    assert_status_code(response_get, 200)

    api_data = response_get.json()

    # ===== VERIFY API DATA =====
    api_errors = []
    if data.get("name") is not None:
        verify_field("API name", api_data.get("name"), data.get("name"), api_errors)

    if data.get("phone") is not None:
        verify_field("API phone", api_data.get("phone"), data.get("phone"), api_errors)

    if data.get("address") is not None:
        verify_field("API address", api_data.get("address"), data.get("address"), api_errors)

    if api_errors:
        raise AssertionError("❌ API VERIFY FAILED:\n" + "\n".join(api_errors))

    print("✅ API data verified successfully")
