"""
Health endpoints for the API.

This module defines a health check endpoint wrapped in a class for documentation purposes.
"""

import datetime

from fastapi import APIRouter

__all__ = ["HealthAPI"]


router = APIRouter()


class HealthAPI:
    """
    A class to encapsulate health check endpoints.

    Use the static method `health_check` to verify that the service is running.
    """

    @staticmethod
    @router.get("/health-check", tags=["Health"])
    async def health_check():
        """
        Health check endpoint.

        Returns:
            dict: A JSON response with the application status and the current UTC time.
        """
        return {"status": "ok", "timestamp": datetime.datetime.utcnow().isoformat()}
