import pytest
from playwright.sync_api import sync_playwright

# =====================================================
# PLAYWRIGHT CORE
# =====================================================

@pytest.fixture(scope="session")
def playwright_instance():
    """Start Playwright once per test session"""
    with sync_playwright() as p:
        yield p


# =====================================================
# API FIXTURES
# =====================================================

@pytest.fixture(scope="session")
def api_context(playwright_instance):
    """API context without authentication"""
    from config.setting import BASE_URL

    context = playwright_instance.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Content-Type": "application/json"
        }
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def api_access_token(api_context):
    """Login once and return access token"""
    from api.auth_api import AuthAPI
    from config.setting import AUTH_USER

    auth_api = AuthAPI(api_context)

    response = auth_api.login({
        "email": AUTH_USER["main"]["email"],
        "password": AUTH_USER["main"]["password"]
    })

    assert response.status == 200, f"Login failed: {response.text()}"
    access_token = response.json().get("accessToken")

    assert access_token, "accessToken not found in response"
    return access_token


@pytest.fixture(scope="session")
def api_context_authenticated(playwright_instance, api_access_token):
    """API context with Authorization header"""
    from config.setting import BASE_URL

    context = playwright_instance.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Authorization": f"Bearer {api_access_token}",
            "Content-Type": "application/json"
        }
    )
    yield context
    context.dispose()


@pytest.fixture(scope="function")
def api_context_change_pw(playwright_instance):
    """
    API context for change-password test
    Login per test to avoid side effects
    """
    from api.auth_api import AuthAPI
    from config.setting import AUTH_USER, BASE_URL

    temp_context = playwright_instance.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={"Content-Type": "application/json"}
    )

    auth_api = AuthAPI(temp_context)
    response = auth_api.login({
        "email": AUTH_USER["change_pw"]["email"],
        "password": AUTH_USER["change_pw"]["password"]
    })

    assert response.status == 200, f"[SETUP] Login failed: {response.text()}"

    access_token = response.json().get("accessToken")
    assert access_token, "[SETUP] accessToken missing"

    auth_context = playwright_instance.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )

    yield auth_context

    auth_context.dispose()
    temp_context.dispose()


@pytest.fixture(scope="session")
def api_context_file(playwright_instance):
    """API context for upload/download file"""
    from config.setting import BASE_URL

    context = playwright_instance.request.new_context(
        base_url=BASE_URL
    )
    yield context
    context.dispose()


# =====================================================
# UI FIXTURES
# =====================================================

@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Launch browser once"""
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """New page per test (safe & isolated)"""
    context = browser.new_context(
        base_url="https://book.anhtester.com/sign-in"
    )
    page = context.new_page()
    yield page
    context.close()

# @pytest.fixture(scope="function")
# def page_authenticated(browser, api_access_token):
#     context = browser.new_context(
#         base_url="https://book.anhtester.com"
#     )

#     page = context.new_page()

#     # 🔴 CỰC QUAN TRỌNG: set token TRƯỚC goto
#     page.add_init_script(
#         f"""
#         window.localStorage.setItem("access_token", "{api_access_token}");
#         """
#     )

#     page.goto("/")  # FE load sau khi đã có token
#     page.wait_for_load_state("networkidle")

#     # 🧪 DEBUG: nếu vẫn bị đá về /sign-in thì fail ngay
#     assert "sign-in" not in page.url, f"Not logged in, current url: {page.url}"

#     yield page
#     context.close()

@pytest.fixture(scope="function")
def page_authenticated(browser, api_access_token):
    context = browser.new_context(
        base_url="https://book.anhtester.com"
    )

    page = context.new_page()

    # 1️⃣ Truy cập origin trước
    page.goto("https://book.anhtester.com")

    # 2️⃣ Set localStorage sau khi đã có origin
    page.evaluate(
        """(token) => {
            window.localStorage.setItem("access_token", token);
        }""",
        api_access_token
    )

    # 3️⃣ Reload để FE đọc token
    page.reload()
    page.wait_for_load_state("networkidle")

    # 4️⃣ Verify login
    assert "sign-in" not in page.url, f"Not logged in, current url: {page.url}"

    yield page
    context.close()

@pytest.fixture
def login(page):
    """Login via UI and return authenticated page"""
    from config.setting import AUTH_USER, BASE_URL
    from pages.login_page import LoginPage

    login_page = LoginPage(page)

    # 🚀 BẮT BUỘC phải navigate trước
    page.goto(f"{BASE_URL}/sign-in")

    login_page.login(
        AUTH_USER["main"]["email"],
        AUTH_USER["main"]["password"]
    )


    return page