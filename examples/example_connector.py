from dotenv import load_dotenv
import os

from src.WatsonxConnector.WatsonxConnector import WatsonxConnector

load_dotenv()

cp4d_url = os.getenv("CP4D_URL")
user_name = os.getenv("USER_NAME")
api_key = os.getenv("API_KEY")
model_id = os.getenv("MODEL_ID")
project_id = os.getenv("PROJECT_ID")


def main():
    example_connector_obj = WatsonxConnector(base_url=cp4d_url,
                                             user_name=user_name,
                                             api_key=api_key,
                                             model_id=model_id,
                                             project_id=project_id
                                             )

    example_connector_obj.set_model_params(temperature=1.2, max_new_tokens=200)

    print(example_connector_obj.get_model_params())

    example_connector_obj.set_model_id("ibm/granite-13b-chat-v2")

    print(example_connector_obj.generate_text("Generate a python code snippet as an example unittest"))

    print(example_connector_obj.get_available_models())


if __name__ == "__main__":
    main()
