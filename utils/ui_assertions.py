# UI Assertions for Profile Update
def assert_update_profile_success(message):
    expected_message = "Profile updated successfully"
    assert message == expected_message, f"Expected message '{expected_message}', but got '{message}'"