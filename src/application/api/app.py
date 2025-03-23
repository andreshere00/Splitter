from fastapi import FastAPI

from src.application.api.routers import (split, health)


app = FastAPI(
    title="Document Splitter API",
    version="0.1.0",
    description="""
        This API allows you to upload a document and split it into chunks using a selected method.
        **Endpoints:**
        - **GET /**: Health check.
        - **POST /documents/split**: Upload and process a document.
    """,
    docs_url="/docs",  # URL for Swagger UI (default)
    redoc_url="/redoc",  # URL for ReDoc (default)
)

# Include the document splitting router with the prefix /documents
app.include_router(split.router, tags=["Documents"])
app.include_router(health.router, tags=["System"])


@app.get("/")
def root():
    """
    Root endpoint to verify that the API is running.
    Returns:
        dict: A message indicating that the API is running.
    """
    return {"message": "Document Splitter API is running"}
