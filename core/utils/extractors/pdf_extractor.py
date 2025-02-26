import io
from langchain_community.document_loaders import PyMuPDFLoader
from tempfile import NamedTemporaryFile
import datetime


class PdfExtractor:
    def __init__(self):
        pass

    def extract_text_with_ocr(self, file_buffer):
        try:
            # Use tesseract-ocr to extract text from the PDF
            import pytesseract
            from pdf2image import convert_from_bytes

            # Convert the PDF to a list of images
            images = convert_from_bytes(file_buffer)

            # Extract text from each image
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)
            return text

        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def load_pdf_from_buffer(self, pdf_bytes: bytes):
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_bytes)
            temp_pdf.seek(0)
            loader = PyMuPDFLoader(temp_pdf.name)
            documents = loader.load()
            return documents
