from fastapi import APIRouter
from app.controllers.reporter_controller import get_reporters

router = APIRouter()

# Reporter-related routes
router.get("/", summary="Get all reporters")(get_reporters)