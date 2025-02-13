# Load ENV variables

import os
from dotenv import load_dotenv

load_dotenv()
# Get Varailbe from .codecraft.env

if os.path.exists(".codecraft.env"):
    load_dotenv(".codecraft.env")
else:
    load_dotenv()

# Check if the variable in the array is present in the .env file
required_varaiables = [
    "OLLAMA_GPU_SERVER",
]

if not all(var in os.environ for var in required_varaiables):
    raise ValueError("Missing required environment variables")

OLLAMA_GPU_SERVER = os.getenv("OLLAMA_GPU_SERVER")
