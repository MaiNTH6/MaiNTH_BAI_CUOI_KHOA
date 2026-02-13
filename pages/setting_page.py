from pydoc import html
import re
from playwright.sync_api import expect
from core.base_page import BasePage

class SettingPage(BasePage):
    # ===== THEME =====
    LIGHT_BTN = "//button[normalize-space()='Light']"
    DARK_BTN = "//button[normalize-space()='Dark']"
    SYSTEM_BTN = "//button[normalize-space()='System']"

    # ===== COLOR =====
    COLOR_FIRST_ITEMS = "//div[@class='MuiBox-root css-h5vkf6']//*[name()='svg']"

    ACTIVE_CLASS = "active"
    HTML = "html"

    # -------- SAVE SETTING --------
    SAVE_BTN = "//button[normalize-space()='Save']"
    SUCCESS_TOAST = ".toast-success"

    # -------- THEME --------
    def change_theme(self, theme: str):
        btn_map = {
            "light": self.LIGHT_BTN,
            "dark": self.DARK_BTN,
            "system": self.SYSTEM_BTN,
        }
        self.click_when_enabled(btn_map[theme])

    def verify_theme(self, theme: str):
        expect(self.page.locator(self.HTML)).to_have_attribute(
            "data-color-scheme", theme
        )

    # -------- COLOR --------
    import re
from playwright.sync_api import expect
from core.base_page import BasePage

class SettingPage(BasePage):
    # ===== THEME =====
    LIGHT_BTN = "//button[normalize-space()='Light']"
    DARK_BTN = "//button[normalize-space()='Dark']"
    SYSTEM_BTN = "//button[normalize-space()='System']"

    # ===== COLOR =====
    COLOR_ITEMS = "//div[@tabindex='0']"


    ACTIVE_CLASS = "active"
    HTML = "html"

    # -------- SAVE SETTING --------
    SAVE_BTN = "//button[normalize-space()='Save']"
    SUCCESS_TOAST = ".toast-success"

    # -------- THEME --------
    def change_theme(self, theme: str):
        btn_map = {
            "light": self.LIGHT_BTN,
            "dark": self.DARK_BTN,
            "system": self.SYSTEM_BTN,
        }
        self.click_when_enabled(btn_map[theme])

    def verify_theme(self, theme: str):
        expect(self.page.locator(self.HTML)).to_have_attribute(
            "data-color-scheme", theme
        )

    # -------- COLOR --------
    def select_first_color(self):
        colors = self.page.locator(self.COLOR_ITEMS)

        # đợi ít nhất 1 màu xuất hiện
        expect(colors.first).to_be_visible(timeout=10000)

        count = colors.count()
        assert count > 0, "No color items found"

        colors.nth(0).click()

    # -------- SAVE SETTING --------
    def save_setting(self):
        self.click_when_enabled(self.SAVE_BTN)
    def verify_save_success(self, expected_message: str):
        toast = self.page.get_by_text(expected_message, exact=True)
        expect(toast).to_be_visible(timeout=5000)

    # Get current theme (light/dark)
    def get_current_theme(self):
        html = self.page.locator("html")
        self.page.wait_for_selector("html[data-color-scheme]")
        return html.get_attribute("data-color-scheme")

   
