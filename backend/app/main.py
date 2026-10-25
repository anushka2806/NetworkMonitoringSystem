from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from backend.app.db.session import init_db
from backend.app.services.tcp_server import start_tcp_server
from backend.app.services.udp_server import start_udp_server
from backend.app.services.monitor import start_monitor
from backend.app.routers import clients, alerts, events, status

app = FastAPI(
    title="Network Monitoring and Fault Detection System",
    description="Monitor clients via TCP probes and UDP heartbeats with ONLINE/WARNING/OFFLINE status",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients.router)
app.include_router(alerts.router)
app.include_router(events.router)
app.include_router(status.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database and start background services"""
    print("[STARTUP] Initializing database...")
    init_db()
    print("[STARTUP] Starting TCP server, UDP receiver, and monitor...")
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()
    udp_thread = threading.Thread(target=start_udp_server, daemon=True)
    udp_thread.start()
    monitor_thread = threading.Thread(target=start_monitor, daemon=True)
    monitor_thread.start()
    print("[STARTUP] All services started successfully")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Network Monitoring System"}

@app.get("/")
async def root():
    return {"message": "Network Monitoring and Fault Detection System API", "docs": "/docs"}
