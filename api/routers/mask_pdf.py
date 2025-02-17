# Create a router for the mask-pdf endpoint
from fastapi import UploadFile, Form, HTTPException
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.services import MaskPdfService
import zipfile
from io import BytesIO


router = APIRouter(
    prefix="/mask-pdf", tags=["mask-pdf"], responses={404: {"description": "Not found"}}
)


@router.post("/")
async def mask_pdf(files: list[UploadFile], prompt: str = Form(...)):
    try:
        mask_pdf_service = MaskPdfService()
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                # Read file bytes
                file_bytes = await file.read()

                # Process PDF with masking
                masked_pdf = mask_pdf_service.mask_pdf_agent(file_bytes, prompt)

                # Add masked PDF to ZIP
                zip_file.writestr(f"masked_{file.filename}", masked_pdf.getvalue())

        zip_buffer.seek(0)  # Reset buffer position

        # Return ZIP file as response
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=masked_pdfs.zip"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDFs: {str(e)}")
