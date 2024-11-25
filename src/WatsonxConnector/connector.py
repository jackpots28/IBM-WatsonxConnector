import urllib3
import requests
import abc

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Singleton(type):
    """
    Singleton metaclass ensuring a single instance of a class.

    Parameters
    ----------
    *args : tuple
        Variable length argument list to pass to the class constructor.
    **kwargs : dict
        Arbitrary keyword arguments to pass to the class constructor.

    Returns
    -------
    instance : object
        The single instance of the class.
    """

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            instance = cls._instances[cls]
            if hasattr(cls, '__allow_reinitialization') and cls.__allow_reinitialization:
                instance.__init__(*args, **kwargs)  # call the init again
        return instance

class WatsonxConnectorInterface(metaclass=abc.ABCMeta):
    """
    :param
    """
    @abc.abstractmethod
    def generate_auth_token(self):
        pass



class WatsonConnector(metaclass=Singleton):

    __slots__ = [
        '_base_url',
        '_api_key',
        '_user_name',
        '_instantiated'
    ]

    def __init__(self, base_url, api_key, user_name):
        self._base_url: str = base_url.replace('https://', '').replace('http://', '')
        self._api_key: str = api_key
        self._user_name: str = user_name
        if hasattr(self, '_instantiated'):
            return
        self._instantiated = True

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value: str):
        self._base_url = value

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = value

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, value: str):
        self._user_name = value


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

