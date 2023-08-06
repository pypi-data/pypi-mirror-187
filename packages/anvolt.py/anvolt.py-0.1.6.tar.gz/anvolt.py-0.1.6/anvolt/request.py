import requests
import json
from typing import Optional, Union, Dict
from anvolt.models.errors import InvalidStatusCode, InvalidResponse, APIOffline


class HttpRequest:
    def __init__(self, **kwargs):
        self.url = "https://anvolt.vercel.app/api/"
        self.custom_url = kwargs.get("custom_url")

        if self.custom_url:
            self.url = self.custom_url

    def get(
        self, route: Optional[str] = None, response: str = "json"
    ) -> Union[Dict, any]:
        try:
            r = requests.get(self.url if not route else self.url + route)

            if not 200 <= r.status_code < 300:
                raise InvalidStatusCode(f"{route} returned {r.status_code}")

            if response == "json":
                return r.json()
            return r
        except json.decoder.JSONDecodeError:
            raise InvalidResponse(
                f"There might be a mistake on our server, or our module is incompatible with the current version"
            )
        except requests.exceptions.ConnectionError:
            raise APIOffline(
                "Please try again later because anvolt-api is currently unavailable."
            )

    def post(
        self, route: Optional[str] = None, json: dict = None, response: str = "json"
    ) -> Union[Dict, any]:
        try:
            r = requests.post(self.url if not route else self.url + route, json=json)

            if not 200 <= r.status_code < 300:
                raise InvalidStatusCode(f"{route} returned {r.status_code}")

            if response == "json":
                return r.json()
            return r
        except json.decoder.JSONDecodeError:
            raise InvalidResponse(
                f"There might be a mistake on our server, or our module is incompatible with the current version"
            )
        except requests.exceptions.ConnectionError:
            raise APIOffline(
                "Please try again later because anvolt-api is currently unavailable."
            )
