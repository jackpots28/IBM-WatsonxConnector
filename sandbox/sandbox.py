import os
from dotenv import load_dotenv
from WatsonxConnector.connector import WatsonConnector


load_dotenv()
url = os.getenv('CP4D_URL')
apikey: str = os.getenv('API_KEY')
username: str = os.getenv('USER_NAME')

connector = WatsonConnector(base_url=url, api_key=apikey, user_name=username)