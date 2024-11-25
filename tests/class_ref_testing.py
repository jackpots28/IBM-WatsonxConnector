import unittest
import os
import urllib3
from dotenv import load_dotenv
from WatsonxConnector.connector import WatsonConnector

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
url: str = os.getenv('CP4D_URL')
apikey: str = os.getenv('API_KEY')
username: str = os.getenv('USER_NAME')

class TestClass(unittest.TestCase):
    obj_1 = WatsonConnector(base_url=url, api_key=apikey, user_name=username)
    obj_2 = WatsonConnector(base_url=url, api_key=apikey, user_name=username)
    def test_singleton_instance(self):
        self.assertEqual(id(self.obj_1), id(self.obj_2))

    def test_gen_auth_token(self):
        result = self.obj_1.generate_auth_token()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    def test_interface_method_checks(self):
        self.assertIsInstance(self.obj_1.generate_auth_token(), str)

if __name__ == '__main__':
    unittest.main()