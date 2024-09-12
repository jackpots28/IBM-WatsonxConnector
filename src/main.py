import requests


class WatsonxConnector(object):
    __slots__ = [
        # --- Set during methods
        '_priv_sys_prompt',
        '_priv_api_version',
        '_priv_full_url',
        '_priv_model_params',
        '_priv_api_token',
        # --- Required on obj creation
        "project_id",
        'base_url',
        'user_name',
        'api_key',
        'model_id',
    ]

    def __init__(self, base_url: str, user_name: str, api_key: str, model_id: str, project_id: str):
        #   --- Public Vars
        self.base_url: str = base_url
        self.user_name: str = user_name
        self.api_key: str = api_key
        self._priv_api_token: str = self.generate_auth_token()
        self.model_id: str = model_id
        #   --- Protected Vars
        # Default system prompt - can be updated with set_system_prompt()
        self._priv_sys_prompt: str = """You are Granite Chat, an AI language model developed by IBM. You are a 
        cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical 
        guidelines and promote positive behavior. You always respond to greetings (for example, hi, hello, g'\''day, 
        morning, afternoon, evening, night, what'\''s up, nice to meet you, sup, etc) with \"Hello! I am Granite 
        Chat, created by IBM. How can I help you today?\". Please do not say anything else and do not start a 
        conversation. ----------------"""
        self._priv_api_version: str = ""
        self._priv_full_url: str = ""
        self.project_id: str = project_id
        # Default model parameters - can be updated with set_model_params()
        self._priv_model_params: dict = {
            "decoding_method": "sample",
            "max_new_tokens": 2000,
            "temperature": 0.5,
            "top_k": 20,
            "top_p": 1,
            "repetition_penalty": 1.0
        }

    #   --- Setters
    def set_system_prompt(self, i_system_prompt: str):
        self._priv_sys_prompt = i_system_prompt

    def set_model_id(self, i_model_id: str):
        self.model_id = i_model_id

    def set_model_params(self, *args, **kwargs):
        self._priv_model_params = {
            "decoding_method": "sample",
            "max_new_tokens": kwargs['max_new_tokens'] | self._priv_model_params['max_new_tokens'],
            "temperature": kwargs['temperature'] | self._priv_model_params['temperature'],
            "top_k": kwargs['top_k'] | self._priv_model_params['top_k'],
            "top_p": kwargs['top_p'] | self._priv_model_params['top_p'],
            "repetition_penalty": kwargs['repetition_penalty'] | self._priv_model_params['repetition_penalty'],
        }

    def set_api_version(self, api_version: str):
        self._priv_api_version = api_version

    def set_project_id(self, project_id: str):
        self.project_id = project_id

    #   --- Getters

    def get_model_id(self) -> str:
        return self.model_id

    #   --- UTILS
    def generate_text(self, query: str, *args, **kwargs) -> str:
        input_query: str = query
        api_version: str = kwargs['api_version'] | "2023-05-29"
        model_id: str = kwargs['model_id'] | self.model_id
        sys_prompt: str = kwargs['sys_prompt'] | self._priv_sys_prompt
        model_params: dict = kwargs['model_params'] | self._priv_model_params
        project_id: str = kwargs['project_id'] | self.project_id

        self._priv_full_url = f"{self.base_url}/ml/v1/text/generation?version={api_version}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._priv_api_token}"
        }

        body = {
            "input": f"""{sys_prompt}\nQuery: {input_query}""",
            "parameters": model_params,
            "model_id": model_id,
            "project_id": project_id,
        }

        response = requests.post(
            self._priv_full_url,
            headers=headers,
            json=body
        )
        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))
        return response.json()

    def generate_auth_token(self) -> str:
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


def main():
    conn = WatsonxConnector(
        base_url="test.somedomain.com",
        user_name="test-user-1",
        api_key="some_api_key_string",
        model_id="some/model",
        project_id="somelongprojectid"
    )

    conn.generate_text("What can you do?")


if __name__ == '__main__':
    main()
