import datetime
from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["System"])


@router.get("/health-check")
async def health_check():
    """
    Health check endpoint.
    Returns a simple JSON response with the application status and current UTC time.
    """
    return {
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
