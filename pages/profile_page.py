from playwright.sync_api import expect

from core.base_page import BasePage
import os


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

    # def verify_profile_updated(self, data: dict):
    #     name = data.get("name")
    #     phone = data.get("phone")
    #     address = data.get("address")

    #     if name is not None:
    #         name_input = self.page.locator(self.NAME_INPUT)
    #         expect(name_input).to_have_value(name)

    #     if phone is not None:
    #         phone_input = self.page.locator(self.PHONE_INPUT)
    #         expect(phone_input).to_have_value(phone)

    #     if address is not None:
    #         address_input = self.page.locator(self.ADDRESS_INPUT)
    #         expect(address_input).to_have_value(address)

    def wait_profile_loaded(self):
        assert "sign-in" not in self.page.url, "User is not logged in"

        expect(
            self.page.locator("form")
        ).to_be_visible(timeout=10000)

    def get_profile_ui_data(self):
        self.wait_profile_loaded()
        division = self.page.locator(self.DIVISION_SELECT).get_attribute("value")
        ward = self.page.locator(self.WARD_SELECT).get_attribute("value")
        address_value = self.page.locator(self.ADDRESS_INPUT).input_value()
        full_address = f"{ward}, {division}"

        return {
            "name": self.page.locator(self.NAME_INPUT).input_value(),
            "phone": self.page.locator(self.PHONE_INPUT).input_value(),
            "address": full_address,
        }

   
