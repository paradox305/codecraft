from core.agents.document_assistant import DocumentAssistant
from core.utils.logger import logger

class HealthCareService:
    def __init__(self):
        self.document_assistant = DocumentAssistant()

    async def upload_report(self, pdf_file):
        # Call the knowledge creation agent
        file_buffer = await pdf_file.read()
        text = self.document_assistant.knowledge_creation_agent(file_buffer)
        logger.info(f"Knowledge creation agent created knowledge: {text}")
        return text