import allure

from api import auth_api
from api import getme_api
from api.profile_api import ProfileAPI
from conftest import api_context_authenticated, page_authenticated
import data
from pages.profile_page import ProfilePage
from utils.api_test_executor import execute_api
from utils.api_assertions import assert_status_code
from utils.excel_reader import read_excel
from components.menu_profile import MenuProfile
from api.getme_api import GetMeAPI
from utils.verify_helpers import verify_field



TEST_DATA_PROFILE = read_excel(
    "data/user_profile.xlsx", sheet_name="Sheet1"
)


@allure.epic("API + UI")
@allure.feature("User")
@allure.story("Update Profile via API and Verify on UI")
def test_api_update_profile_verify_ui(
    api_context_authenticated,
    login,
   
):
    data = TEST_DATA_PROFILE[0]

    # ===== API UPDATE =====
    profile_api = ProfileAPI(api_context_authenticated)

    response, _ = execute_api(
        profile_api.update_profile,
        payload=data,
        endpoint=profile_api.ENDPOINT,
        attach=True
    )
    assert_status_code(response, 200)

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
    verify_field("API name", api_data.get("name"), data.get("name"), api_errors)
    verify_field("API phone", api_data.get("phone"), data.get("phone"), api_errors)
    verify_field("API address", api_data.get("address"), data.get("address"), api_errors)

    if api_errors:
        raise AssertionError("❌ API VERIFY FAILED:\n" + "\n".join(api_errors))

    print("✅ API data verified successfully")

    # ===== UI VERIFY =====
    page = login
    # page.goto("/user-management/my-profile")

    profile_page = ProfilePage(page)
    # Click on avatar to go to Profile Page
    MenuProfile(page).open_profile()
    ui_data = profile_page.get_profile_ui_data()

    ui_errors = []
    verify_field("UI name", ui_data["name"], api_data["name"], ui_errors)
    verify_field("UI phone", ui_data["phone"], api_data["phone"], ui_errors)
    verify_field("UI address", ui_data["address"], api_data["address"], ui_errors)

    if ui_errors:
        raise AssertionError("❌ UI VERIFY FAILED:\n" + "\n".join(ui_errors))

    print("🎉 UI data verified successfully")



    