# Test upload avatar functionality
import pytest
import allure
from config.setting import BASE_URL, AUTH_USER
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from components.menu_profile import MenuProfile
@allure.epic("UI")
@allure.feature("User")
@allure.story("Upload Avatar")
def test_upload_avatar(page):
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
    # Upload avatar
    avatar_file_path = "data/image_avatar/avatar-2.jpg"
    profile_page.upload_avatar(avatar_file_path)
    profile_page.save_profile()
    profile_page.verify_update_success("Updated profile successfully.")
