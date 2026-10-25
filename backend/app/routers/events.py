from fastapi import APIRouter
from backend.app.db.session import fetch_all

router = APIRouter(tags=["events"])

@router.get("/events")
async def get_events(limit: int = 50):
    events = fetch_all(
        "SELECT * FROM event_history ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    return events
