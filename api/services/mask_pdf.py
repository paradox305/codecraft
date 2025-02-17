from core.agents.mask_pdf import MaskPdf

class MaskPdfService:
    def __init__(self):
        self.mask_pdf = MaskPdf()

    def mask_pdf_agent(self, input_pdf, prompt):
        try:
            return self.mask_pdf.mask_text_on_pdf(input_pdf, prompt)
        except Exception as e:
            raise ValueError(f"Error in mask_pdf_agent: {e}")
        