# IBM Watsonx API wrapper package for calling text generation and embedding requests

[![Python][python-badge]](https://www.python.org/)

---

## Usage / Examples

```python

example_connector_obj = WatsonxConnector(base_url=cp4d_url,
                                         user_name=user_name,
                                         api_key=api_key,
                                         model_id=model_id,
                                         project_id=project_id
                                         )

for model, model_type in example_connector_obj.get_available_models().items():
    print(f"{model}: {model_type}")

example_connector_obj.set_model_params(temperature=0.7, max_new_tokens=800)
print(example_connector_obj.get_model_params())

print(example_connector_obj.generate_text("Write an example python unittest"))

example_connector_obj.set_model_id(model_id="ibm/slate-125m-english-rtrvr")
for embed in example_connector_obj.generate_embedding(["something", "something else"]):
    print(embed)
```

## Example output from above:

codellama/codellama-34b-instruct-hf: text_generation
ibm/granite-13b-chat-v2: text_generation
ibm/slate-125m-english-rtrvr: embedding
ibm/slate-30m-english-rtrvr: embedding
meta-llama/llama-3-70b-instruct: text_generation

{'decoding_method': 'sample', 'max_new_tokens': 800, 'temperature': 0.7, 'top_k': 20, 'top_p': 0.9, 'repetition_penalty': 1.1}

```python
import unittest
from mymodule import my_function

class MyTest(unittest.TestCase):

    def test_my_function(self):
        result = my_function('hello world')
        self.assertEqual(result, 'Hello World')

if __name__ == '__main__':
    unittest.main()
```
This is an example of a simple Python unit test using the `unittest` module. In this case, we define a new class called `MyTest` which inherits from `unittest.TestCase`. This allows us to use all the methods provided by the `unittest.TestCase` class, such as `setUp()` and `tearDown()`.

Inside the `test_my_function()` method, we call the function we want to test (`my_function`) and provide it with a string argument ('hello world' in this case). We then use the `assertEqual()` method to check if the result of the function call matches the expected value ('Hello World' in this case).

Finally, we run the tests by calling `unittest.main()` in our script. This will execute all the tests defined in the current module (in this case, just the one test defined in `MyTest`).

In summary, this is a basic example of how to write a unit test in Python using the `unittest` module. Unit testing is a great way to ensure that your functions are working as intended and catching issues early in the development process.

`[-0.024465775, -0.0329509, -0.00046468992, -0.017108368, ...  0.017113319, 0.01991029, -0.010878863, 0.005576967]
[-0.037240397, -0.04046932, -0.03115683, -0.034350585, ... 0.020475477, 0.05027425, 0.006514402, 0.0150749]`


---

### List of available class methods:

- set_system_prompt()
- set_model_id()
- set_model_params()
- set_api_version()
- set_project_id()
- get_model_id()
- get_auth_token()
- get_model_params()
- get_available_models()
- check_model_type()
- generate_text()
- generate_embedding()
- generate_auth_token()

## License

[Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)

[python-badge]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
