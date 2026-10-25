# 06 - FastAPI Backend (Non-blocking)

## Goals
- FastAPI app serving REST API with real DB data
- Run TCP server, UDP receiver, monitor without blocking HTTP requests
- CORS enabled for React frontend

## Startup
In `backend/app/main.py`:
```python
@app.on_event("startup")
async def startup_event():
    # init DB
    init_db()
    # start background threads/tasks
    start_tcp_server()      # thread
    start_udp_server()      # thread  
    start_monitor()         # thread
```
Use `threading.Thread(target=..., daemon=True).start()` for blocking socket loops.

## API Endpoints (Real Data)
- `GET /health` - status
- `GET /clients` - all clients with all fields
- `GET /clients/{id}` - single client
- `GET /alerts` - all alerts (order by timestamp desc)
- `GET /events` - event_history (order by timestamp desc, limit)
- `GET /status/summary` - counts by status (ONLINE/WARNING/OFFLINE), alerts count
- `GET /clients/{id}/probes` - probe history for client

All queries hit SQLite directly, return JSON.

## CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Files
- `backend/app/main.py`
- `backend/app/routers/` (clients, alerts, events)
- `backend/app/config.py`
- `backend/app/db/session.py`
- `backend/run.py` (uvicorn)
- `backend/requirements.txt` (fastapi, uvicorn, pydantic)
