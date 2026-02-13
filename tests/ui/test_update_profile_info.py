# tests/ui/test_update_profile.py
import pytest
import allure

from config.setting import BASE_URL, AUTH_USER
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from components.menu_profile import MenuProfile

from utils.excel_reader import read_excel

TEST_DATA = read_excel("data/profile_ui_data.xlsx", "Sheet1")

@allure.epic("UI")
@allure.feature("User")
@allure.story("Update Profile")
@pytest.mark.parametrize("data", TEST_DATA)
def test_update_profile(page, data):
    login_page = LoginPage(page)
    profile_page = ProfilePage(page)

    # Login
    login_page.goto(BASE_URL)

    login_page.login(
        AUTH_USER["main"]["email"],
        AUTH_USER["main"]["password"]
    )
    login_page.verify_login_success()


    # Click on avatar to go to Profile Page
    MenuProfile(page).open_profile()


    # Update profile information
    profile_page.fill_profile(data)
    profile_page.save_profile()
    profile_page.verify_update_success(data.get("expected_message"))


