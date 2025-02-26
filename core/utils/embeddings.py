from langchain_huggingface import HuggingFaceEmbeddings
class Embeddings:
    def __init__(self):
        self.huggingface_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        