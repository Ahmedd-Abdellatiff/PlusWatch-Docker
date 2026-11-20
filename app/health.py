import requests

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }


def check_website(url):
    try:
        response = requests.get(url, timeout=10)

        return {
            "status": "up" if response.ok else "down",
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "error_message": None
        }

    except requests.RequestException as e:
        return {
            "status": "down",
            "status_code": None,
            "response_time": None,
            "error_message": str(e)
        }