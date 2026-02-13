#  ============== STATUS CODE =================
def assert_status_code(response, expected_status, message=None):
    actual = response.status
    assert actual == expected_status, (
        message or f"Expected status {expected_status}, got {actual}"
    )

    

#  ============== LOGIN SUCCESS ================
def assert_login_success(response):
    assert_status_code(response, 200)

    try:
        body = response.json()
    except Exception:
        assert False, f"Response is not valid JSON: {response.text()}"

    assert isinstance(body, dict), f"Response body is not dict: {body}"
    assert "accessToken" in body, f"Missing accessToken in response: {body}"
    assert body["accessToken"], "accessToken is empty"



#  ============== LOGIN RESPONSE ================
def assert_login_response(response, data):
    try:
        body = response.json()
    except Exception:
        assert False, f"Response is not valid JSON: {response.text()}"

    # -------- Status code --------
    expected_status = int(data.get("expected_status"))
    assert response.status == expected_status, (
        f"Expected status {expected_status}, got {response.status}"
    )

    # -------- Success case --------
    if expected_status == 200:
        # check accessToken
        assert "accessToken" in body, f"Missing accessToken in response: {body}"
        assert body["accessToken"], "accessToken is empty"

        # check expired
        if data.get("expected_expired"):
            assert "exp" in body, f"Missing 'exp' in response: {body}"
            assert body["exp"] == data["expected_expired"]

    # -------- Error case --------
    else:
        # check msg
        assert "msg" in body, f"Missing 'msg' in response: {body}"
        # check expected message
        if data.get("expected_message"):
            assert body["msg"] == data["expected_message"]
        # check fields
        if data.get("expected_fields"):
            assert "fields" in body, f"Missing 'fields' in response: {body}"

            expected_fields = [
                field.strip()
                for field in data["expected_fields"].split(",")
            ]

            for field in expected_fields:
                assert field in body["fields"], (
                    f"Missing field '{field}' in response fields: {body['fields']}"
                )
# ============== RESPONSE TIME =================
def assert_response_time(duration, max_time, api_name=None):
    # Check duration is a number
    assert isinstance(duration, (int, float)), (
        f"Invalid duration type: {type(duration)}"
    )
    # Check duration within limit
    assert duration <= max_time, (
        f"[{api_name or 'API'}] Response time too long: "
        f"{duration}s > {max_time}s"
    )

#  ============= GET ME RESPONSE =================
def assert_me_response(response):
    body = response.json()

    assert response.status == 200
    assert "email" in body
    assert "id" in body


# ============== PROFILE DATA =================

# Hàm check profile data response
def assert_profile_data(response_data, expected_payload):
    # Backend chỉ trả msg
    assert "msg" in response_data, "Response missing 'msg'"
    assert response_data["msg"] == "Updated profile successfully."

# Hàm check get me data response
def assert_getme_data(data):
    expected_fields = [
        "id",
        "name",
        "email",
        "phone",
        "address",
        "avatarUrl",
        "config"
    ]

    for field in expected_fields:
        assert field in data, f"Missing field '{field}' in get me response"

    assert isinstance(data["id"], str)
    assert isinstance(data["name"], str)
    assert isinstance(data["email"], str)
    assert isinstance(data["phone"], str)
    assert isinstance(data["address"], str)
    assert isinstance(data["avatarUrl"], (str, type(None)))
    assert isinstance(data["config"], dict)

# Hàm check profile data response
def assert_profile_me_data(actual: dict, expected: dict):
    for field in ["name", "phone", "address"]:
        if expected.get(field) is not None:
            assert actual.get(field) == expected.get(field), \
                f"{field} mismatch: {actual.get(field)} != {expected.get(field)}"

#  ============== CHANGE PASSWORD RESPONSE =================
def assert_change_password_response(response, data):
    try:
        body = response.json()
    except Exception:
        assert False, f"Response is not valid JSON: {response.text()}"

    expected_status = int(data.get("expected_status", 200))

    # ===== Status code =====
    assert response.status == expected_status, (
        f"Expected status {expected_status}, got {response.status}"
    )

    # ===== Success =====
    if expected_status == 200:
        assert "msg" in body, f"Missing msg in success response: {body}"
        assert body["msg"], "msg should not be empty"

    # ===== Validation / error =====
    else:
        assert (
            "msg" in body or "fields" in body
        ), f"Expected msg or fields in error response, got: {body}"