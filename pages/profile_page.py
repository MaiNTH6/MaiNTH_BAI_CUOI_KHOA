from playwright.sync_api import expect

from core.base_page import BasePage
import os
import re



class ProfilePage(BasePage):
    NAME_INPUT = "input[name='name']"
    PHONE_INPUT = "input[name='phone']"
    DIVISION_SELECT = "//input[@id='address-division']"
    WARD_SELECT = "//input[@id='address-ward']"
    ADDRESS_INPUT = "//textarea[@id='address']"
    SAVE_BTN = "//button[normalize-space()='Save Profile']"
    SUCCESS_TOAST = ".toast-success"

    AVATAR_INPUT = "input[type='file'][name='avatar']"

    def fill_profile(self, data: dict):
        self.fill_if_not_none(self.NAME_INPUT, data.get("name"))
        self.fill_if_not_none(self.PHONE_INPUT, data.get("phone"))
        self.fill_autocomplete(self.DIVISION_SELECT, data.get("division"))
        self.fill_autocomplete(self.WARD_SELECT, data.get("ward"))    
        self.fill_if_not_none(self.ADDRESS_INPUT, data.get("address"))

    def upload_avatar(self, file_path: str):
        abs_path = os.path.abspath(file_path)
        self.page.locator(self.AVATAR_INPUT).set_input_files(abs_path)

    def save_profile(self):
        self.click_when_enabled(self.SAVE_BTN)

    def verify_update_success(self, expected_message):
        toast = self.page.get_by_text(expected_message, exact=True)
        expect(toast).to_be_visible(timeout=5000)
        # Chụp ảnh
        self._take_screenshot("test_update_profile", folder="profile")



    def wait_profile_loaded(self):
        assert "sign-in" not in self.page.url, "User is not logged in"

        expect(
            self.page.locator("form")
        ).to_be_visible(timeout=10000)

    # def get_profile_ui_data(self):
    #     self.wait_profile_loaded()
    #     division = self.page.locator(self.DIVISION_SELECT).get_attribute("value")
    #     ward = self.page.locator(self.WARD_SELECT).get_attribute("value")
    #     address_value = self.page.locator(self.ADDRESS_INPUT).input_value()
    #     full_address = f"{ward}, {division}"

    #     return {
    #         "name": self.page.locator(self.NAME_INPUT).input_value(),
    #         "phone": self.page.locator(self.PHONE_INPUT).input_value(),
    #         "address": full_address,
    #     }

    def get_profile_ui_data(self):
        self.wait_profile_loaded()

        # ===== Name =====
        name_locator = self.page.locator(self.NAME_INPUT)
        expect(name_locator).to_be_visible(timeout=5000)
        name = name_locator.input_value().strip()

        # ===== Phone =====
        phone_locator = self.page.locator(self.PHONE_INPUT)
        expect(phone_locator).to_be_visible(timeout=5000)
        phone = phone_locator.input_value().strip()

        # ===== Address =====
        address_locator = self.page.locator(self.ADDRESS_INPUT)
        expect(address_locator).to_be_visible(timeout=5000)
        address_value = address_locator.input_value().strip()

        # ===== Division (quan trọng nhất - tránh flaky) =====
        division_locator = self.page.locator(self.DIVISION_SELECT)

        # Đợi division có giá trị thật sự (không rỗng)
        expect(division_locator).to_have_value(
            re.compile(r".+"), timeout=5000
        )

        division = division_locator.input_value().strip()
        ward_locator = self.page.locator(self.WARD_SELECT)
        expect(ward_locator).to_have_value(
            re.compile(r".+"), timeout=5000
        )
        ward = ward_locator.input_value().strip()


        # Build address giống format API
        full_address = f"{ward}, {division}".strip()

        return {
            "name": name,
            "phone": phone,
            "address": full_address,
        }

   
