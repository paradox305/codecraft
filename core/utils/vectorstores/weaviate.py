import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore as Weaviate
from core.utils.embeddings import Embeddings
from core.utils.env import get_env_variable
from core.utils.logger import logger


class WeaviateVectorStore:
    def __init__(self):
        self.client = weaviate.connect_to_local(host=get_env_variable("WEAVIATE_HOST"))
        self.embeddings = Embeddings().huggingface_embeddings

    def add_documents_to_vector_store(self, index_name, documents, **kwargs):
        weaviate = Weaviate(
            client=self.client,
            index_name=index_name,
            text_key="test",
            embedding=self.embeddings,
        )
        # Add documents to the vector store
        ids = weaviate.add_documents(documents=documents)
        return ids

    def search(self, query, index_name):
        weaviate = Weaviate(
            client=self.client,
            index_name=index_name,
            text_key="test",
            embedding=self.embeddings,
        )
        # Search for relevant documents
        logger.debug(f"Searching for query: {query}")
        docs = weaviate.similarity_search(query)
        
        return [doc.page_content for doc in docs]
