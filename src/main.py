from dataclasses import dataclass
import requests
import typing
import os

from loguru import logger


class WatsonxConnector(object):
    __slots__ = [
        '_c_priv_sys_prompt',
        '_c_priv_api_base',
        '_c_priv_model_id',
        '_c_priv_api_version',
        '_c_priv_full_url',
        '_c_priv_project_id',
        '_c_priv_model_params',
        'c_base_url',
        'c_usr_name',
        'c_api_key',
        'c_api_token',
    ]

    def __init__(self, base_url: str, usr_name: str, api_key: str, ):
        #   --- Public Vars
        self.c_base_url: str = base_url
        self.c_usr_name: str = usr_name
        self.c_api_key: str = api_key
        self.c_api_token: str = self.generate_auth_token()
        #   --- Protected Vars
        self._c_priv_sys_prompt: str = ""
        self._c_priv_api_base: str = ""
        self._c_priv_model_id: str = ""
        self._c_priv_api_version: str = ""
        self._c_priv_full_url: str = ""
        self._c_priv_project_id: str = ""
        self._c_priv_model_params: dict = dict()

    def __str__(self):
        return

    def __repr__(self):
        return

    #   --- Setters
    def set_system_prompt(self, i_system_prompt: str):
        self._c_priv_sys_prompt = i_system_prompt

    def set_model_id(self, i_model_id: str):
        self._c_priv_model_id = i_model_id

    def set_model_params(self, i_repetition_penalty: float, i_temperature: float, i_top_k: int,
                         i_top_p: int, i_max_new_tokens: int,):
        self._c_priv_model_params = {
            "decoding_method": "sample",
            "max_new_tokens": i_max_new_tokens,
            "temperature": i_temperature,
            "top_k": i_top_k,
            "top_p": i_top_p,
            "repetition_penalty": i_repetition_penalty
        }

    def set_api_version(self, i_api_version: str):
        self._c_priv_api_version = i_api_version

    def set_project_id(self, i_project_id: str):
        self._c_priv_project_id = i_project_id

    #   --- Getters
    def get_api_base(self) -> str:
        return self._c_priv_api_base

    def get_model_id(self) -> str:
        return self._c_priv_model_id

    #   --- UTILS
    def text_generation(self, *args, **kwargs) -> str:
        i_api_version: str = kwargs['i_api_version']
        i_model_id: str = kwargs['i_model_id']
        i_sys_prompt: str = kwargs['i_sys_prompt']
        i_model_params: dict = kwargs['i_model_params']
        i_project_id: str = kwargs['i_project_id']

        #   --- Verify vars are set if needed
        if self._c_priv_api_version == "":
            if i_api_version is not None:
                self.set_api_version(i_api_version)
            else:
                logger.error("API VERSION - not set")
        if self._c_priv_model_id == "":
            if i_model_id is not None:
                self.set_model_id(i_model_id)
            else:
                logger.error("Model ID - not set")
        if self._c_priv_sys_prompt == "":
            if i_sys_prompt is not None:
                self.set_system_prompt(i_sys_prompt)
            else:
                logger.error("SYSTEM PROMPT not set")
        if self._c_priv_model_params is {}:
            if i_model_params is not None:
                self.set_model_params(i_model_params)
            else:
                logger.error("MODEL PARAMS not set")
        if self._c_priv_project_id == "":
            if i_project_id is not None:
                self.set_project_id(i_project_id)
            else:
                logger.error("PROJECT ID not set")

        self._c_priv_api_base = f"{self.c_base_url}/ml/v1/text/generation?{self._c_priv_api_version}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.c_api_token}"
        }

        body = {
            "input": f"""{self._c_priv_sys_prompt}""",
            "parameters": self._c_priv_model_params,
            "model_id": self._c_priv_model_id,
            "project_id": self._c_priv_project_id,
        }

        response = requests.post(
            self._c_priv_api_base,
            headers=headers,
            json=body
        )

        return "TEST"

    def generate_auth_token(self) -> str:
        return requests.post(
            url=f"https://{self.c_base_url}/icp4d-api/v1/authorize",
            headers={
                "cache-control": "no-cache",
                "Content-Type": "application/json"
            },
            json={
                "username": f"{self.c_usr_name}",
                "api_key": f"{self.c_api_key}"
            },
            verify=False
        ).json()["token"]


def main():
    conn = WatsonxConnector(
        base_url="test.somedomain.com",
        usr_name="test-user-1",
        api_key="some_api_key_string"
    )

    conn.set_system_prompt(i_system_prompt="SOMETHING")
    conn.set_model_id(i_model_id="TEST_MODEL")
    # print(conn.generate_auth_token())
    print(conn.get_model_id())


if __name__ == '__main__':
    main()
