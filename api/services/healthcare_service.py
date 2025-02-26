from core.agents.document_assistant import DocumentAssistant
from core.utils.logger import logger


class HealthCareService:
    def __init__(self):
        self.document_assistant = DocumentAssistant()

    async def upload_report(self, pdf_file):
        # Call the knowledge creation agent
        file_buffer = await pdf_file.read()
        text = self.document_assistant.knowledge_creation_agent(
            file_buffer, index_name="healthcare"
        )
        logger.info(f"Knowledge creation agent created knowledge: {text}")
        return text

    async def search_agent(self, query):
        logger.info(f"Search agent called with query: {query}")
        # Call the search agent
        system_prompt = """You are a healthcare assistant. You are given a query and a set of documents. Your task is to answer the query based on the documents. You should only use the information provided in the documents to answer the query."""
        text = self.document_assistant.search_agent(query, index_name="healthcare", system_prompt=system_prompt)
        logger.info(f"Search agent created knowledge: {text}")
        return text
