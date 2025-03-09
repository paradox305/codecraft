from abc import abstractmethod
import os
import re
import weaviate
import time
import uuid
from langchain_weaviate.vectorstores import WeaviateVectorStore as Weaviate
from core.utils.embeddings import Embeddings
from core.utils.env import get_env_variable
from core.utils.logger import logger


class WeaviateVectorStore:
    def __init__(self):
        self.client = weaviate.connect_to_local(host=get_env_variable("WEAVIATE_HOST"),port=get_env_variable("WEAVIATE_PORT"))
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
    
    @staticmethod
    def rename_to_valid_weaviate_class_name(file_path: str) -> str:
        """
        Renames a given file to a valid Weaviate class name.
        
        1. Extracts the filename (without extension).
        2. Removes all non-alphanumeric characters.
        3. Ensures it starts with an uppercase letter.
        4. Prepends 'C' if the first character is a digit.
        5. Renames the file in the given path.
        
        Returns:
            str: The new valid filename.
        
        Raises:
            ValueError: If no valid class name can be generated.
        """
        # Extract directory, filename, and extension
        dir_path, full_filename = os.path.split(file_path)
        filename, ext = os.path.splitext(full_filename)

        # Remove all non-alphanumeric characters
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', filename)

        # Ensure a valid name is generated
        if not cleaned:
            raise ValueError(f"Error: No valid Weaviate class name can be generated from '{filename}'")

        # If the first character is a digit, prepend 'C'
        if cleaned[0].isdigit():
            cleaned = 'C' + cleaned

        # Capitalize the first character
        cleaned = cleaned[0].upper() + cleaned[1:]

        # Construct new filename with original extension
        new_filename = f"{cleaned}{ext}"
        new_file_path = os.path.join(dir_path, new_filename)

        # Rename the file
        os.rename(file_path, new_file_path)
        
        print(f"File renamed: {file_path} → {new_file_path}")
        return new_filename
    
    @staticmethod
    def generate_unique_weaviate_index(file_path: str) -> str:
        """
        Generates a unique and valid Weaviate index name for a given file upload.

        1. Extracts the filename (without extension).
        2. Removes all non-alphanumeric characters.
        3. Ensures it starts with an uppercase letter.
        4. Appends a unique identifier (UUID + timestamp).
        5. Returns the generated index name.

        Returns:
            str: A valid, unique Weaviate index name.
        """
        # Extract filename (without extension)
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # Remove all non-alphanumeric characters
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', filename)

        # Ensure there's a valid name
        if not cleaned:
            cleaned = "File"  # Default name if no valid chars remain

        # If the first character is a digit, prepend 'C'
        if cleaned[0].isdigit():
            cleaned = 'C' + cleaned

        # Capitalize first letter
        cleaned = cleaned[0].upper() + cleaned[1:]

        # Generate unique suffix (UUID + Timestamp)
        unique_id = str(uuid.uuid4().hex[:8])  # Short UUID
        timestamp = str(int(time.time()))  # Current timestamp

        # Combine name with unique suffix
        index_name = f"{cleaned}_{unique_id}_{timestamp}"

        return index_name