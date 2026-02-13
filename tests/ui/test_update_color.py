import pytest
import allure
from pages.setting_page import SettingPage
from components.menu_profile import MenuProfile

@allure.epic("UI")
@allure.feature("User")
@allure.story("Update Theme Color")
def test_select_first_color(login):
    page = login

    MenuProfile(page).open_setting()
    setting = SettingPage(page)


    setting.select_first_color()
    setting.save_setting()
    setting.verify_save_success("Updated profile successfully.")

