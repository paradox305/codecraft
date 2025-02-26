from langchain_text_splitters import CharacterTextSplitter
from datetime import datetime
from core.utils.logger import logger


class Chunker:
    def __init__(self):
        pass

    def chunk_text(self, documents, chunk_size=1000):
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)  # Correct method

        # Add creationdate property to each chunk
        for chunk in chunks:
            chunk.metadata["creationdate"] = datetime.now().replace(microsecond=0).isoformat() + "Z"

        logger.info(f"Chunked text into {len(chunks)} chunks")

        return chunks