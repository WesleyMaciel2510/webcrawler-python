from fastapi import HTTPException
from app.services.document_service import search_documents_by_term

async def search_documents(term: str):
    documents = search_documents_by_term(term)
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    return {"documents": documents}