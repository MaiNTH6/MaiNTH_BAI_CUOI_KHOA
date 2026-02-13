import os
import time
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def fill(self, locator: str, value: str):
        el = self.page.locator(locator)
        expect(el).to_be_visible()
        el.fill(value)

    def fill_select(self, locator, value):
        if value is not None:
            self.page.locator(locator).select_option(label=value)
    
    def fill_autocomplete(self, locator, value):
        if value is None:
            return

        input_field = self.page.locator(locator)

        input_field.click()
        input_field.fill("")      # clear nếu có value cũ
        input_field.fill(value)

    # chọn option hiển thị
        self.page.get_by_role("option", name=value).click()


    def fill_if_not_none(self, locator: str, value):
        if value is None:
            return
        self.fill(locator, value)

    def click(self, locator: str):
        el = self.page.locator(locator)
        expect(el).to_be_visible()
        el.click()

    def click_when_enabled(self, locator: str):
        el = self.page.locator(locator)
        expect(el).to_be_visible()
        expect(el).to_be_enabled()
        el.click()

    def wait_visible(self, locator: str, timeout=5000):
        try:
            expect(self.page.locator(locator)).to_be_visible(timeout=timeout)
        except Exception:
            self._take_screenshot("wait_visible_failed")
            raise

    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text()

    def _take_screenshot(self, filename: str, folder=None):
        import os
        import time

        if folder is None:
            folder = "others"

        screenshot_dir = os.path.join("screenshots", folder)
        os.makedirs(screenshot_dir, exist_ok=True)

        path = os.path.join(
            screenshot_dir,
            f"{filename}_{int(time.time())}.png"
        )

        self.page.screenshot(path=path)
        print(f"[SCREENSHOT] Lưu tại: {path}")
