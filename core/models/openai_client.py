import os
from langchain_openai import ChatOpenAI

class OpenAIClient:
    def __init__(self, model_name, **kwargs):
        self.model_names = ["gpt-4o-mini"]
        self.model_name = model_name
    def get_client(self,**kwargs):
        if not os.environ.get("OPENAI_API_KEY"):
            raise "OpenAI api key is not loaded"
        if self.model_name in self.model_names:
            return ChatOpenAI(model=self.model_name, temperature=0,max_retries=2, **kwargs)
