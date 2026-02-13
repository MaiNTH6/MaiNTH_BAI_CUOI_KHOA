====================================================================
        PLAYWRIGHT PYTHON AUTOMATION FRAMEWORK (API + UI)
====================================================================

Project Name : AT04
Author       : Nguyen Thi Hoang mai
Version      : 1.0

--------------------------------------------------------------------
1. OVERVIEW
--------------------------------------------------------------------
Framework tự động hóa kiểm thử cho hệ thống <AnhTester Book Management> bao gồm:
- API Testing
- UI Testing
- API + UI Integration Testing

Mục tiêu:
- StorageState / Token reuse
- Logs, Report, Screenshot
- Excel data cho profile update

Link system:
- UI: https://book.anhtester.com/user-management/my-profile
- API: https://book.anhtester.com/swagger#tag/authentication-management/POST/api/login

--------------------------------------------------------------------
2. TECHNOLOGY STACK
--------------------------------------------------------------------
- Language      : Python 3.9+
- UI Automation : Playwright
- API Automation: Playwright APIRequestContext
- Test Runner   : Pytest
- Report        : Allure
- Test Data     : Excel (openpyxl)
- Pattern       : POM + API Client Layer
- CI/CD         : Jenkins / GitHub Actions

--------------------------------------------------------------------
3. PROJECT STRUCTURE
--------------------------------------------------------------------
project-root/
│
├── tests/
│   ├── api/
│   │   ├── test_login_api.py
            test_api_get_me.py
│   │   ├── test_profile_api.py
│   │   └── test_change_password_api.py
│   │
│   ├── ui/
│   │   ├── test_my_profile_ui.py
│   │   └── test_setting_account_ui.py
│   │
│   └── integration/
│       ├── test_api_update_ui_verify.py
│       ├── test_ui_update_api_verify.py
│       └── test_theme_persist.py
│
├── pages/
│   ├── base_page.py
│   ├── my_profile_page.py
│   └── setting_account_page.py
│
├── api/
│   ├── base_api.py  -- Chỉ gửi request
│   ├── auth_api.py
│   └── profile_api.py
│
├── utils/
│   ├── config_reader.py
│   ├── excel_reader.py
│   ├── logger.py
│   └── assertion_helper.py
│
├── data/
│   ├── profile_update.xlsx
│   └── users.json
│
├── storage/
│   └── auth_state.json
│
├── reports/
│   ├── allure-results
│   └── screenshots
│
├── config/
│   └── config.yaml
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.txt

--------------------------------------------------------------------
4. TEST SCOPE
--------------------------------------------------------------------

4.1 API TEST
--------------------------------------------------
- Login API
    * POST /api/login → lấy access token
- Get user info
    * GET /api/me
- Update profile
    * PATCH /api/profile
        - name
        - phone
        - address
- Change password
    * Valid password
    * Invalid password

--------------------------------------------------
4.2 UI TEST
--------------------------------------------------
My Profile:
- Update Name
- Update Phone
- Update Address
- Upload Avatar (image)

Setting Account:
- Change Theme (Light / Dark / System)
- Change UI Color

--------------------------------------------------
4.3 API + UI INTEGRATION TEST
--------------------------------------------------
- API Update Profile → UI verify data
- UI Update Profile → API GET verify
- UI Change Theme → Reload page → Verify persisted setting

--------------------------------------------------------------------
5. AUTHENTICATION STRATEGY
--------------------------------------------------------------------
- Login qua API để lấy token
- Lưu token / cookies vào storageState
- UI test sử dụng storageState để bypass login
- Giảm thời gian chạy test & tăng stability

File:
    storage/auth_state.json

--------------------------------------------------------------------
6. TEST DATA MANAGEMENT
--------------------------------------------------------------------
- Profile update sử dụng Excel file:
    data/profile_update.xlsx

- Mỗi row = 1 test data
    name | phone | address | expected_result

- Excel được load qua:
    utils/excel_reader.py

--------------------------------------------------------------------
7. LOGGING & REPORTING
--------------------------------------------------------------------
- Log framework:
    + API request / response
    + UI actions
    + Assertion result

- Screenshot:
    + Tự động capture khi test FAIL
    + Lưu tại reports/screenshots

- Report:
    + Allure Report
    + Có log + screenshot + step

--------------------------------------------------------------------
8. RUN TEST
--------------------------------------------------------------------
Chạy toàn bộ test:
    pytest

Chạy API test:
    pytest tests/api

Chạy UI test:
    pytest tests/ui

Chạy Integration test:
    pytest tests/integration

Sinh Allure report:
    pytest --alluredir=reports/allure-results

Mở report:
    allure serve reports/allure-results

--------------------------------------------------------------------
9. CI/CD
--------------------------------------------------------------------
Framework sẵn sàng tích hợp:
- Jenkins
- GitHub Actions

Pipeline:
- Checkout source
- Install dependencies
- Run API tests
- Generate storageState
- Run UI & Integration tests
- Publish Allure report

--------------------------------------------------------------------
10. BEST PRACTICES
--------------------------------------------------------------------
- API test độc lập UI
- UI test không phụ thuộc data hardcode
- Không dùng time.sleep()
- Page Object chỉ chứa locator & action
- Assertion rõ ràng, có message
- Không commit secret / token thật

--------------------------------------------------------------------
11. CONTACT
--------------------------------------------------------------------
Maintainer : <Your Name>
Email      : <your_email>

====================================================================
