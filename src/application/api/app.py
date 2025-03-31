from fastapi import FastAPI

from src.application.api.routers import health, split

app = FastAPI(
    title="Document Splitter API",
    version="0.1.0",
    description="""
This API allows you to upload a document and split it into chunks using a selected method.

**Endpoints:**
- **`GET` - `/health-check`**: Health check.
- **`POST` - `/documents/split`**: Upload and process a document.
""",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register application routers
app.include_router(split.router, tags=["Documents"])
app.include_router(health.router, tags=["Health"])


@app.get("/", tags=["System"])
def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Document Splitter API is running"}
