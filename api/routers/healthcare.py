# Heathcare Assistant API
from fastapi import APIRouter, HTTPException, UploadFile
from api.services.healthcare_service import HealthCareService

router = APIRouter(
    prefix="/healthcare",
    tags=["healthcare"],
    responses={404: {"description": "Not found"}},
)

# Initialize the HealthCareService
healthcare_service = HealthCareService()


# Router to upload a PDF report
@router.post("/upload-report")
async def upload_report(file: UploadFile):
    try:
        report = await healthcare_service.upload_report(file)
        return {"message": "Report uploaded successfully", "index_name": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.get("/search")
async def search(query: str, index_name: str):
    try:
        result = await healthcare_service.search_agent(query, index_name=index_name)
        return {"message": "Search successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")
