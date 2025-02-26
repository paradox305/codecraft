from core.utils.extractors.pdf_extractor import PdfExtractor

class DocumentAssistant:
    def __init__(self):
        self.pdf_extractor = PdfExtractor()

    def knowledge_creation_agent(self, pdf_file):
        # Extract text from PDF
        text = self.pdf_extractor.extract_text_with_ocr(pdf_file)
        return text
