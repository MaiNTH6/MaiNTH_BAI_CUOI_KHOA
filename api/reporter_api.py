# api/reporter_api.py
import json


try:
    import allure
except ImportError:
    allure = None


class APIReporter:
    @staticmethod
    def attach_api_info(
        method,
        endpoint,
        payload,
        response,
        response_time=None,
        request_data=None
    ):
        if not allure:
            return

        with allure.step(f"{method} {endpoint}"):
            if payload:
                allure.attach(
                    str(payload),
                    name="Request Payload",
                    attachment_type=allure.attachment_type.JSON
                )

            allure.attach(
                str(response.status),
                name="Response Status",
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                response.text(),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(request_data, indent=2, ensure_ascii=False),
                name="Request Data",
                attachment_type=allure.attachment_type.JSON
    )

            if response_time is not None:
                allure.attach(
                    f"{response_time}s",
                    name="Response Time",
                    attachment_type=allure.attachment_type.TEXT
                )
