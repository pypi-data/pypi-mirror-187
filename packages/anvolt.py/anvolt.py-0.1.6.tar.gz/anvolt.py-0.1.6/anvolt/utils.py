from anvolt.request import HttpRequest
from anvolt.models.errors import InvalidNumber
from typing import Optional, Tuple, List
import os


class Utils:
    def __init__(self):
        self.http_request = HttpRequest()

    def _ensure_folder_exist(self, folder_name: str) -> None:
        os.makedirs(folder_name, exist_ok=True)

    def _save_image(self, file_name: str, url: str) -> str:
        response = HttpRequest(custom_url=url).get(route=None, response=None)
        with open(f"AnVoltPicture/{file_name}.{url[-3:]}", "wb") as file:
            file.write(response.content)
        return f"File {file_name} saved in AnVoltPicture"

    def produce(
        self, total: int, route: str, request_type: str = "url"
    ) -> Tuple[List[str], List[dict]]:
        if not 2 <= total <= 15:
            raise InvalidNumber(
                "Can't generate more than 15 or less than 1 request at a time."
            )

        urls, responses = [], []
        for _ in range(total):
            res = self.http_request.get(route=route)
            urls.append(res[request_type])
            responses.append(res)

        return urls, responses

    def save(
        self, route: str, total: int = 1, filename: Optional[str] = None
    ) -> List[Tuple[str, str]]:
        self._ensure_folder_exist("AnVoltPicture")

        if not filename:
            filename = route.split("/")[1].title()

        if not 1 <= total <= 15:
            raise InvalidNumber(
                "Can't generate more than 15 or less than 1 request at a time."
            )

        if total == 1:
            req = self.http_request.get(route=route)
            return self._save_image(file_name=filename, url=req.get("url"))

        image_urls, image_paths = [], []
        for i in range(total):
            req = self.http_request.get(route=route)
            url = req.get("url")

            file_name = f"{filename}_{i+1}"
            self._save_image(file_name, url)
            image_urls.append(url)
            image_paths.append(file_name)

        return [image_urls, image_paths]
