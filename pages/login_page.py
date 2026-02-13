# pages/login_page.py
from core.base_page import BasePage


class LoginPage(BasePage):
    URL = "/sign-in"

    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    LOGIN_BTN = "button[type='submit']"

    SUCCESS_TOAST = "text=Login successfully"

    def goto(self, base_url):
        super().goto(base_url + self.URL)

    def login(self, email, password):
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def verify_login_success(self):
        self.wait_visible(self.SUCCESS_TOAST)