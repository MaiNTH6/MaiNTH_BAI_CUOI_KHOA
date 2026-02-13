class UploadAPI:
    ENDPOINT_AVATAR = "/api/file"

    def __init__(self, api_context):
        self.api_context = api_context

    def upload_avatar(self, image_path: str, email: str):
        with open(image_path, "rb") as f:
            file_bytes = f.read()

        upload_path = f"/$avatar-image/{email}"  # 🔥 BẮT BUỘC $

        response = self.api_context.post(
            self.ENDPOINT_AVATAR,
            multipart={
                "files": {
                    "name": "avatar-2.jpg",
                    "mimeType": "image/jpeg",
                    "buffer": file_bytes
                },
                "path": upload_path   # text field
            }
        )

        print("STATUS:", response.status)
        print("BODY:", response.text())

        assert response.status == 200, response.text()
        return response.json()["paths"][0]
