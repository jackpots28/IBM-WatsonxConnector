import urllib3
import requests
import abc
from dataclasses import dataclass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


class WatsonxConnectorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'generate_auth_token') and
                callable(subclass.generate_auth_token))



class WatsonConnector(Singleton):
    __slots__ = [
        'base_url',
        'api_key',
    ]

    def __init__(self, base_url, api_key):
        self.base_url: str = base_url.replace('https://', '').replace('http://', '').strip('/')
        self.api_key: str = api_key

    @property
    def base_url(self):
        return self.base_url

    @base_url.setter
    def base_url(self, value: str):
        self.base_url = value


    @property
    def api_key(self):
        return self.api_key

    @api_key.setter
    def api_key(self, value: str):
        self.api_key = value


    def generate_auth_token(self, api_key=None, user_name=None) -> str:
        if api_key is not None:
            self.api_key = api_key

        if user_name is not None:
            self.user_name = user_name

        return requests.post(
            url=f"https://{self.base_url}/icp4d-api/v1/authorize",
            headers={
                "cache-control": "no-cache",
                "Content-Type": "application/json"
            },
            json={
                "username": f"{self.user_name}",
                "api_key": f"{self.api_key}"
            },
            verify=False
        ).json()["token"]

