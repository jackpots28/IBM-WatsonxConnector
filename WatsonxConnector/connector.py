import requests
import urllib3
from typing import List, Final

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TODO - change model_id to not be required on object instantiation, but error more gracefully for if model_id
#  is not set and is required when calling a class method.
#  On model_id set - check against models on cluster and fail gracefully if not present

# TODO - need to cleanup type hints for method output definitions (overall)
class WatsonxConnector(object):
    __slots__ = [
        # --- Set during methods
        '_priv_sys_prompt',
        '_priv_user_prompt',
        '_priv_api_version',
        '_priv_full_url',
        '_priv_model_params',
        '_priv_api_token',
        '_priv_deployment_id',
        '_priv_custom_model_text_generation_api_url',

        # --- Required on obj creation
        "project_id",
        'base_url',
        'user_name',
        'api_key',
        'model_id',
    ]

    def __init__(self, base_url: str, user_name: str, api_key: str, project_id: str, model_id: str = ""):
        #   --- Public Vars
        self.base_url: str = base_url.replace("https://", "").replace("http://", "")
        self.user_name: str = user_name
        self.api_key: str = api_key
        self._priv_api_token: str = self.generate_auth_token()
        self.model_id: str = model_id
        #   --- Protected Vars
        # Default system prompt - can be updated with set_system_prompt()
        self._priv_sys_prompt: str = \
            """
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
        Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
        Please ensure that your responses are socially unbiased and positive in nature.

        If a question does not make any sense, or is not factually coherent, explain why instead of answering 
        something not correct. If you don't know the answer to a question, please don't share false 
        information. 
        
        Once you answer a question, do not continue on with repeats.
        ----------------"""
        self._priv_user_prompt: str = "QUESTION: "
        self._priv_api_version: str = ""
        self._priv_full_url: str = ""
        self.project_id: str = project_id
        # Default model parameters - can be updated with set_model_params()
        self._priv_model_params: dict = {
            "decoding_method": "sample",
            "max_new_tokens": 1000,
            "temperature": 0.4,
            "top_k": 20,
            "top_p": 0.9,
            "repetition_penalty": 1.1
        }
        self._priv_deployment_id: str = ""

    text_generation_api_url: Final[str] = "/ml/v1/text/generation?version="
    embed_generation_api_url: Final[str] = "/ml/v1/text/embeddings?version="

    #   --- Setters
    # TODO - Need to elaborate on the setting of user/system prompts for better tooling in prompt engineering
    def set_system_prompt(self, system_prompt: str):
        self._priv_sys_prompt = system_prompt

    def set_user_prompt(self, user_prompt: str):
        self._priv_user_prompt = user_prompt

    def set_model_id(self, model_id: str):
        self.model_id = model_id

    def set_model_params(self, **kwargs):
        if "max_new_tokens" in kwargs:
            self._priv_model_params["max_new_tokens"] = kwargs["max_new_tokens"]

        if "temperature" in kwargs:
            self._priv_model_params["temperature"] = kwargs["temperature"]

        if "top_k" in kwargs:
            self._priv_model_params["top_k"] = kwargs["top_k"]

        if "top_p" in kwargs:
            self._priv_model_params["top_p"] = kwargs["top_p"]

        if "repetition_penalty" in kwargs:
            self._priv_model_params["repetition_penalty"] = kwargs["repetition_penalty"]

    def set_api_version(self, api_version: str):
        self._priv_api_version = api_version

    def set_project_id(self, project_id: str):
        self.project_id = project_id

    def set_deployment_id(self, deployment_id: str):
        self._priv_deployment_id = deployment_id

    #   --- Getters
    def get_model_id(self) -> str:
        return self.model_id

    def get_auth_token(self) -> str:
        return self._priv_api_token

    def get_model_params(self) -> dict:
        return self._priv_model_params

    def get_sys_prompt(self) -> str:
        return self._priv_sys_prompt

    def get_user_prompt(self) -> str:
        return self._priv_user_prompt

    def get_params(self) -> str:
        return "\n".join([f"{k}: {v}" for k, v in self._priv_model_params.items()])

    def get_deployment_id(self) -> str | None:
        return self._priv_deployment_id

    #   --- UTILS
    def generate_text(self, query: str) -> str:
        input_query: str = query
        api_version: str = "2023-05-29"
        api_url_function: str = self.text_generation_api_url
        model_id: str = self.model_id
        sys_prompt: str = self._priv_sys_prompt
        user_prompt: str = self._priv_user_prompt
        model_params: dict = self._priv_model_params
        project_id: str = self.project_id

        self._priv_full_url = f"https://{self.base_url}{api_url_function}{api_version}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._priv_api_token}"
        }

        body = {
            "input": f"""{sys_prompt}\n{user_prompt}{input_query}\n""",
            "parameters": model_params,
            "model_id": model_id,
            "project_id": project_id,
        }

        if self.check_model_type(model_id=model_id, model_type="text_generation") \
                or self.check_model_type(model_id=model_id, model_type="text_chat"):
            response = requests.post(
                self._priv_full_url,
                headers=headers,
                json=body,
                verify=False
            )
            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))

            return response.json()['results'][0]['generated_text']
        else:
            raise Exception("MODEL TYPE IS NOT SUPPORTED FOR --TEXT-- GENERATION")

    def generate_text_custom_model(self, query: str) -> str:
        input_query: str = query
        api_version: str = "2023-05-29"
        sys_prompt: str = self._priv_sys_prompt
        user_prompt: str = self._priv_user_prompt
        model_params: dict = self._priv_model_params
        if WatsonxConnector.get_deployment_id(self) is None:
            raise Exception("Deployment ID accessible")
        else:
            api_url_function = f"/ml/v1/deployments/{WatsonxConnector.get_deployment_id(self)}/text/generation?version="

        self._priv_full_url = f"https://{self.base_url}{api_url_function}{api_version}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._priv_api_token}"
        }

        body = {
            "input": f"""{sys_prompt}\n{user_prompt}{input_query}\n""",
            "parameters": model_params,
        }

        response = requests.post(
            self._priv_full_url,
            headers=headers,
            json=body,
            verify=False
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        return response.json()['results'][0]['generated_text']

    def generate_embedding(self, phrase: str | List[str]) -> List[float]:
        input_string: str | List[str] = phrase
        api_version: str = "2024-05-02"
        api_url_function: str = self.embed_generation_api_url
        model_id: str = self.model_id
        project_id: str = self.project_id
        body: dict = {}

        self._priv_full_url = f"https://{self.base_url}{api_url_function}{api_version}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._priv_api_token}"
        }

        if isinstance(phrase, str):
            body = {
                "inputs": [input_string],
                "parameters": {
                    "truncate_input_tokens": 128
                },
                "model_id": model_id,
                "project_id": project_id,
            }
        elif isinstance(phrase, list):
            body = {
                "inputs": input_string,
                "parameters": {
                    "truncate_input_tokens": 128
                },
                "model_id": model_id,
                "project_id": project_id,
            }

        if self.check_model_type(model_id=model_id, model_type="embedding"):
            response = requests.post(
                self._priv_full_url,
                headers=headers,
                json=body,
                verify=False
            )
            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))

            return [item['embedding'] for item in response.json()['results']]
        else:
            raise Exception("MODEL TYPE IS NOT SUPPORTED FOR --EMBEDDING-- GENERATION")

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

    def get_available_models(self) -> dict:
        api_version: str = "2020-09-01"
        api_url_function: str = "/ml/v1/foundation_model_specs?version="

        response = requests.get(
            url=f"https://{self.base_url}{api_url_function}{api_version}",
            verify=False
        ).json()

        model_functions = [func['functions'][:] for func in response['resources'] if len(func['functions'][:]) > 0]
        model_names = [model_id['model_id'] for model_id in response['resources'] if len(model_id['functions'][:]) > 0]

        return {model: func[0]['id'] for (model, func) in zip(model_names, model_functions)}

    # TODO - need to check if model_id is set on class vars first and error more gracefully
    def check_model_type(self, model_id: str, model_type: str) -> bool:
        if self.model_id is not None:
            if self.get_available_models()[model_id] == model_type:
                return True
            else:
                return False
        else:
            return False
