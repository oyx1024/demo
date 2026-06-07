"""HTTP 请求封装"""
import requests
import json
from common.logger import logger
from config.config import config


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.base_url
        self.timeout = config.timeout
        # 可在此设置默认 headers
        self.session.headers.update({
            "User-Agent": "ApiTestFramework/1.0"
        })

    def request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        logger.info(f"➡️  {method.upper()} {url}")
        if "json" in kwargs:
            logger.debug(f"   Body: {json.dumps(kwargs['json'], ensure_ascii=False)}")

        resp = self.session.request(method, url, **kwargs)

        logger.info(f"⬅️  {resp.status_code}")
        try:
            body = resp.json()
            logger.debug(f"   Response: {json.dumps(body, ensure_ascii=False)[:500]}")
        except Exception:
            body = resp.text
            logger.debug(f"   Response: {resp.text[:500]}")

        return resp

    def get(self, endpoint: str, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)


client = ApiClient()
