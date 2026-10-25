from fastapi import APIRouter
from backend.app.db.session import fetch_all

router = APIRouter(tags=["alerts"])

@router.get("/alerts")
async def get_alerts():
    alerts = fetch_all("SELECT * FROM alerts ORDER BY timestamp DESC")
    return alerts
