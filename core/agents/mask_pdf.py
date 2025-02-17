import io
from core.utilis.logger import logger
from core.models.ollama import OllamaClient


class MaskPdf:
    def __init__(self):
        import cv2
        import pytesseract
        from pdf2image import convert_from_bytes
        import numpy as np
        from PIL import Image

        self.cv2 = cv2
        self.pytesseract = pytesseract
        self.convert_from_bytes = convert_from_bytes
        self.np = np
        self.Image = Image
        self.llm_client = OllamaClient(
            model_name="llama3.2",
            gpu_server="http://localhost:11434",
            kwargs={"temperature": 0.7, "cache": False},
        ).get_client()

    def mask_words(self, words, prompt):
        try:
            instruction = f"""
                        Your task is to mask the following information from the pdf, you will be given text snippets and you have to determine if the text needs to be masked or not. Answer in one word only, either true or false, Donot add any explaination.
                        Fields to mask: 
                        {prompt}
                        Text to evaluate:
                        {words}
                        """
            # Use Ollama client to determine if the text should be masked
            response = self.llm_client.invoke(instruction)
            # Check if "true" appears in the response (case insensitive)
            if "true" in response.content.lower():
                logger.info(
                    f"Text to be masked: {words} , LLM Response: {response.content}"
                )
                return True
            else:
                return False
        except Exception as e:
            raise ValueError(f"Error in mask_words: {e}")

    def mask_text_on_pdf(self, input_pdf, prompt, dpi=600):
        try:
            # Convert PDF to images
            images = self.convert_from_bytes(input_pdf, dpi=dpi)

            output_pdf = io.BytesIO()
            masked_images = []
            for img in images:
                # Convert to OpenCV format
                img_cv = self.np.array(img)
                img_gray = self.cv2.cvtColor(img_cv, self.cv2.COLOR_RGB2GRAY)

                # Perform OCR to detect words
                h, w, _ = img_cv.shape
                data = self.pytesseract.image_to_data(
                    img_gray, output_type=self.pytesseract.Output.DICT
                )
                # Create a context of next and previous words with a rolling window of 8 words
                statement = ""
                for i, word in enumerate(data["text"]):
                    statement += word + " "
                    words = statement.strip().split()
                    if len(words) > 8:
                        statement = " ".join(words[-8:])
                    elif len(words) == 1:
                        # Add padding to reach 8 words
                        statement = " ".join(words + [" "] * 7)
                    if self.mask_words(words=statement, prompt=prompt):
                        x, y, w, h = (
                            data["left"][i],
                            data["top"][i],
                            data["width"][i],
                            data["height"][i],
                        )
                        self.cv2.rectangle(
                            img_cv, (x, y), (x + w, y + h), (0, 0, 0), -1
                        )  # Black box mask
                masked_images.append(self.Image.fromarray(img_cv))
            # Creater a new PDF with masked images and return the whole pdf with first page
            masked_images[0].save(
                output_pdf, "PDF", save_all=True, append_images=masked_images[1:]
            )
            output_pdf.seek(0)
            logger.info("PDF masked successfully")
            return output_pdf
        except Exception as e:
            raise e
