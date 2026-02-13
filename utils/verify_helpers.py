# utils/verify_helpers.py
def verify_field(field_name, actual, expected, errors: list):
    if actual == expected:
        print(f"[OK] {field_name}: {actual}")
    else:
        error_msg = (
            f"[ERROR] {field_name} mismatch | "
            f"expected='{expected}' | actual='{actual}'"
        )
        print(error_msg)
        errors.append(error_msg)