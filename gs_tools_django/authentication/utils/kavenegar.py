import logging
from typing import Self

import httpx
import ujson

from gs_tools_django.settings import KAVENEGAR_API_TEMPLATE_LOGIN_VERIFICATION

DEFAULT_TIMEOUT = 10


class KavenegarAPI:
    version = "v1"
    host = "api.kavenegar.com"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "utf-8",
    }

    def __init__(self: Self, apikey: str, timeout: int | None = None, proxies=None):
        self.apikey = apikey
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.proxies = proxies

    def _pars_params_to_json(self: Self, params: dict):
        formatted_params = {}
        for key, value in params.items():
            if isinstance(value, dict | list | tuple):
                formatted_params[key] = ujson.dumps(value)
            else:
                formatted_params[key] = value
        return formatted_params

    def _request(self: Self, action: str, method: str, params: dict | None = None):
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = self._pars_params_to_json(params)
        url = f"https://{self.host}/{self.version}/{self.apikey}/{action}/{method}.json"
        content = httpx.post(
            url,
            headers=self.headers,
            auth=None,
            data=params,
            timeout=self.timeout,
            proxies=self.proxies,
        ).content
        try:
            response = ujson.loads(content.decode("utf-8"))
            if response["return"]["status"] == 200:
                return response["entries"]
        except ValueError as e:
            raise ValueError() from e

    def sms_send(self: Self, params: dict | None = None):
        return self._request("sms", "send", params)

    def sms_status(self: Self, params: dict | None = None):
        return self._request("sms", "status", params)

    def sms_statuslocalmessageid(self: Self, params: dict | None = None):
        return self._request("sms", "statuslocalmessageid", params)

    def sms_cancel(self: Self, params: dict | None = None):
        return self._request("sms", "cancel", params)

    def sms_receive(self: Self, params: dict | None = None):
        return self._request("sms", "receive", params)

    def verify_lookup(self: Self, params: dict | None = None):
        return self._request("verify", "lookup", params)


class KavenegarSMSProvider:
    def __init__(self: Self, auth_token: str):
        self.client = KavenegarAPI(auth_token)

    def send_sms(self, to_phone_number: str, content: str):
        try:
            self.client.verify_lookup(
                params={
                    "receptor": to_phone_number,
                    "token": content,
                    "template": KAVENEGAR_API_TEMPLATE_LOGIN_VERIFICATION,
                },
            )
        except Exception as e:
            logging.warning(e)
