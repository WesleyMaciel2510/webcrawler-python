from fastapi import FastAPI
from app.routes.movie_routes import router as movie_router
from app.routes.reporter_routes import router as reporter_router
from app.routes.document_routes import router as document_router

app = FastAPI()

app.include_router(movie_router, prefix="/api/movies", tags=["movies"])
app.include_router(movie_router, prefix="/api/movies/searchByName", tags=["movies"])

app.include_router(reporter_router, prefix="/api/reporters", tags=["reporters"])
app.include_router(document_router, prefix="/api/documents", tags=["documents"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the WebCrawler API!"}