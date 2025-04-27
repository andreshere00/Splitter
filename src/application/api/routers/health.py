"""
Health endpoints for the API.
"""

import datetime

from fastapi import APIRouter

__all__ = ["HealthAPI", "router"]

router = APIRouter()


class HealthAPI:
    """
    Simple health-check router.
    """

    @staticmethod
    @router.get("/health-check", tags=["Health"])
    async def health_check():
        return {
            "status": "ok",
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        }
