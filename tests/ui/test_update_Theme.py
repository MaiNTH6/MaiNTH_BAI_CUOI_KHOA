import pytest
import allure
from pages.setting_page import SettingPage
from components.menu_profile import MenuProfile


@allure.epic("UI")
@allure.feature("User")
@allure.story("Update Theme")
@pytest.mark.parametrize("theme", ["dark", "light"])
def test_update_theme(login, theme):
    page = login

    MenuProfile(page).open_setting()
    setting_page = SettingPage(page)

    setting_page.change_theme(theme)
    setting_page.verify_theme(theme)

