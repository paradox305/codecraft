from core.models.openai_client import OpenAIClient
from core.models.ollama_client import OllamaClient

class LLM:
    def __init__(self, provider, **kwargs):
        # Map provider names to their corresponding client classes
        self.providers = {
            "openai": OpenAIClient,
            "ollama": OllamaClient
        }
        if provider not in self.providers:
            raise ValueError(f"Unsupported provider: {provider}")
        self.provider = provider
        # Store any additional arguments (e.g., gpu_server for Ollama)
        self.client_args = kwargs

    def get_client(self, model_name):
        # Retrieve the appropriate client class
        client_class = self.providers[self.provider]
        # Instantiate the client with the model name and any additional parameters
        client_instance = client_class(model_name, **self.client_args)
        # Return the built client (assuming each client has a get_client method)
        return client_instance.get_client()

