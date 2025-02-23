from fastapi import APIRouter, HTTPException
from typing import List
from app.services.reporter_service import ReportersService
from app.models.reporter import Reporter

router = APIRouter()
reporters_service = ReportersService()

@router.get("/reporters", response_model=List[Reporter])
async def get_reporters():
    try:
        # Fetch reporters from the service
        reporters = reporters_service.get_reporters()

        # Transform the list of reporter names into Reporter objects
        reporter_objects = [Reporter(name=name, organization="Unknown") for name in reporters]

        # Return the response
        return {
            "success": True,
            "count": len(reporter_objects),
            "data": reporter_objects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error fetching reporters",
        )