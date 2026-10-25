from fastapi import APIRouter
from backend.app.db.session import fetch_all, fetch_one

router = APIRouter(tags=["clients"])

@router.get("/clients")
async def get_clients():
    clients = fetch_all("SELECT * FROM clients ORDER BY id ASC")
    return clients

@router.get("/clients/{client_id}")
async def get_client(client_id: int):
    client = fetch_one("SELECT * FROM clients WHERE id = ?", (client_id,))
    if not client:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/clients/{client_id}/probes")
async def get_client_probes(client_id: int, limit: int = 50):
    probes = fetch_all(
        "SELECT * FROM response_time_probe_history WHERE client_id = ? ORDER BY probe_at DESC LIMIT ?",
        (client_id, limit)
    )
    return probes
