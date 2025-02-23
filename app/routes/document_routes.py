from fastapi import APIRouter
from app.controllers.document_controller import search_documents

router = APIRouter()

# Document-related routes
router.get("/", summary="Search documents by term")(search_documents)