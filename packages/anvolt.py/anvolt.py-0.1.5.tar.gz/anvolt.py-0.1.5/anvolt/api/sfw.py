from anvolt.request import HttpRequest
from anvolt.models.response import Responses
from anvolt.models.enums import Route
from anvolt.utils import Utils
from typing import Optional


class Sfw:
    def __init__(self, client_id: Optional[str], client_secret: Optional[str] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.http_request = HttpRequest()
        self.utils = Utils()

    def _make_request(self, route: str, produce: Optional[int] = None) -> Responses:
        url, original_response = (
            self.utils.produce(total=produce, route=route)
            if produce
            else (
                self.http_request.get(route=route).get("url"),
                self.http_request.get(route=route),
            )
        )
        status_response = (
            [response.get("status_response") for response in original_response]
            if produce
            else original_response.get("status_response")
        )

        return Responses(
            url=url,
            status_response=status_response,
            original_response=original_response,
        )

    def bite(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.BITE.value, produce=produce)

    def headpat(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.HEADPAT.value, produce=produce)

    def highfive(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.HIGHFIVE.value, produce=produce)

    def hug(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.HUG.value, produce=produce)

    def poke(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.POKE.value, produce=produce)

    def run(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.RUN.value, produce=produce)

    def slap(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.SLAP.value, produce=produce)

    def smile(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.SMILE.value, produce=produce)
