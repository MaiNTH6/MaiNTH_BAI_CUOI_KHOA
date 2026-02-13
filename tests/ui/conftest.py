import pytest
from pages.login_page import LoginPage
from config.setting import BASE_URL, AUTH_USER


@pytest.fixture
def login(page):
    login_page = LoginPage(page)
    login_page.goto(BASE_URL)
    login_page.login(
        AUTH_USER["main"]["email"],
        AUTH_USER["main"]["password"]
    )
    login_page.verify_login_success()
    return page
