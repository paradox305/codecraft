class OllamaClient:
    def __init__(self, model_name, gpu_server, **kwargs):
        from langchain_ollama import ChatOllama

        self.ChatOllama = ChatOllama
        self.model_name = model_name
        self.gpu_server = gpu_server
        self.kwargs = kwargs

    def get_client(self):
        return self.ChatOllama(
            model=self.model_name, gpu_server=self.gpu_server, **self.kwargs
        )