import pytest
import allure

from components.menu_profile import MenuProfile
from pages.setting_page import SettingPage


@allure.epic("UI")
@allure.feature("User Settings")
@allure.story("Change Theme Persistence")
@allure.severity(allure.severity_level.CRITICAL)
def test_change_theme_persist_after_reload(login):
    """
    Test flow:
    1. Login
    2. Navigate to Setting page
    3. Change theme (Light <-> Dark)
    4. Reload page
    5. Verify theme is persisted
    """

    page = login
    setting_page = SettingPage(page)

    # Step 1: Open Setting page
    with allure.step("Open Setting page from avatar menu"):
        MenuProfile(page).open_setting()

    # Step 2: Get current theme
    with allure.step("Get current theme value"):
        current_theme = setting_page.get_current_theme()
        assert current_theme in ["light", "dark", "system"], \
            f"Unexpected theme value: {current_theme}"

    # Step 3: Toggle theme
    with allure.step("Change theme"):
        new_theme = "dark" if current_theme == "light" else "light"

        setting_page.change_theme(new_theme)
        setting_page.save_setting()
        setting_page.verify_save_success("Updated profile successfully.")
        setting_page.verify_theme(new_theme)

    # Step 4: Reload page
    with allure.step("Reload page"):
        page.reload()
        page.wait_for_load_state("networkidle")


    # Step 5: Verify theme persisted
    with allure.step("Verify theme persisted after reload"):
        persisted_theme = setting_page.get_current_theme()
        assert persisted_theme == new_theme, \
            f"Theme not persisted. Expected: {new_theme}, Actual: {persisted_theme}"

    print("✅ Theme persistence verified successfully")