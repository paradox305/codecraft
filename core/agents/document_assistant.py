from core.utils.extractors.pdf_extractor import PdfExtractor
from core.utils.vectorstores.weaviate import WeaviateVectorStore
from core.utils.chunkers import Chunker
from langchain.prompts import PromptTemplate
from core.models.ollama import OllamaClient


class DocumentAssistant:
    def __init__(self):
        self.pdf_extractor = PdfExtractor()
        self.vector_store = WeaviateVectorStore()
        self.chunker = Chunker()
        self.llm_client = OllamaClient(
            model_name="llama3.2",
            gpu_server="http://localhost:11434",
            kwargs={"temperature": 0, "cache": False},
        ).get_client()

    def knowledge_creation_agent(self, pdf_file, index_name):
        # Extract text from PDF
        docs = self.pdf_extractor.load_pdf_from_buffer(pdf_file)

        # Chunk text into smaller chunks
        chunks = self.chunker.chunk_text(documents=docs)

        # Save the chunks to the vector store
        saved_ids = self.vector_store.add_documents_to_vector_store(
            index_name=index_name, documents=chunks
        )
        return saved_ids

    def search_agent(self, query, index_name, system_prompt):
        # Search for relevant documents
        search_results = self.vector_store.search(query, index_name)

        # Create a system prompt and configure the Agent
        master_prompt = f"""{system_prompt} 
                        {search_results}
                        {query}
                        """

        # Create a prompt template with system prompt and user prompt
        prompt_template = PromptTemplate(template=master_prompt)

        # Use the prompt template to prompt
        prompt = prompt_template.format(query=query, search_results=search_results, system_prompt=system_prompt)

        # Use the prompt to generate a response from llm
        response = self.llm_client.invoke(prompt)

        return response.content
