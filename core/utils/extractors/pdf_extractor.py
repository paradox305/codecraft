class PdfExtractor:
    def __init__(self):
        pass

    def extract_text_with_ocr(self, file_buffer):
        try:
            # Use tesseract-ocr to extract text from the PDF
            import pytesseract
            from PIL import Image
            import tempfile

            # Use the buffer as a file-like object
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(file_buffer)
                temp_pdf.flush()
                # Use pytesseract to extract text from the PDF
                text = pytesseract.image_to_string(Image.open(temp_pdf.name))
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
