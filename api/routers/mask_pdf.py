# Create a router for the mask-pdf endpoint
from fastapi import UploadFile
from  fastapi import APIRouter

router = APIRouter(prefix="/mask-pdf", tags=["mask-pdf"],  responses={404: {"description": "Not found"}})

@router.post("/")
async def mask_pdf(file: UploadFile):
    try:
        return {"message": "PDF masked successfully"}
    except Exception as e:
        return {"error": str(e)}
