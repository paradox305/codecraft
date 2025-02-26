import os
from dotenv import load_dotenv
load_dotenv()

def get_env_variable(variable_name):
    return os.getenv(variable_name)

required_env_variables = ['WEAVIATE_HOST']

# Check if all required environment variables are set
for variable in required_env_variables:
    if get_env_variable(variable) is None:
        raise ValueError(f"Environment variable {variable} is not set.")