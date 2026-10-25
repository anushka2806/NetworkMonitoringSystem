import os

# Server Configuration
TCP_SERVER_HOST = "0.0.0.0"
TCP_SERVER_PORT = 5000

UDP_SERVER_HOST = "0.0.0.0"
UDP_SERVER_PORT = 5001

FASTAPI_HOST = "127.0.0.1"
FASTAPI_PORT = 8000

# Database
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "monitor.db")

# Heartbeat Configuration
HEARTBEAT_INTERVAL = 5  # seconds - client sends heartbeat every 5s
HEARTBEAT_WARNING_THRESHOLD = 10  # seconds - >10s since last heartbeat -> WARNING
HEARTBEAT_OFFLINE_THRESHOLD = 15  # seconds - >15s since last heartbeat -> OFFLINE

# TCP Probe Configuration
PROBE_INTERVAL = 10  # seconds - server probes clients every 10s
PROBE_WARNING_CONSECUTIVE = 2  # >=2 consecutive failed probes -> WARNING
PROBE_OFFLINE_CONSECUTIVE = 4  # >=4 consecutive failed probes -> OFFLINE

# Monitor Configuration
MONITOR_CHECK_INTERVAL = 2  # seconds - monitor checks every 2-3s
