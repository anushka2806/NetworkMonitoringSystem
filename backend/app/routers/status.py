from fastapi import APIRouter
from backend.app.db.session import fetch_all

router = APIRouter(tags=["status"])

@router.get("/status/summary")
async def get_status_summary():
    # Count by status
    status_counts = fetch_all("SELECT status, COUNT(*) as cnt FROM clients GROUP BY status")
    counts = {"ONLINE": 0, "WARNING": 0, "OFFLINE": 0}
    for row in status_counts:
        if row['status'] in counts:
            counts[row['status']] = row['cnt']
    
    total_alerts = fetch_all("SELECT COUNT(*) as total FROM alerts")[0]['total']
    unacked = fetch_all("SELECT COUNT(*) as unacked FROM alerts WHERE acknowledged = 0")[0]['unacked']
    total_clients = sum(counts.values())
    
    return {
        "total_clients": total_clients,
        "online": counts["ONLINE"],
        "warning": counts["WARNING"],
        "offline": counts["OFFLINE"],
        "total_alerts": total_alerts,
        "unacknowledged_alerts": unacked
    }
