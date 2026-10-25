# 07 - Client Agents

## Goals
Create simple clients for demo (explainable in viva).

## TCP Client (`client/tcp_client.py`)
Responsibilities:
1. Connect to TCP server (host:port from config)
2. Send registration: `{"type":"REGISTER","client_name":"client-01","ip_address":"127.0.0.1"}`
3. Maintain persistent connection (keep socket open)
4. Listen for probe requests from server: `{"type":"PROBE","ts":...}`
5. Respond with probe response: `{"type":"PROBE_RESP","ts": <original>}`
6. Handle reconnect on disconnect (simple)

## UDP Client (`client/udp_heartbeat.py`)
Responsibilities:
1. Send heartbeat every HEARTBEAT_INTERVAL (5s)
2. Payload: `{"type":"HEARTBEAT","client_name":"client-01","ip_address":"127.0.0.1","ts": time.time()}`
3. Send to UDP_SERVER_HOST:UDP_SERVER_PORT
4. Run in loop

## Notes
- Use same client_name across TCP and UDP for matching
- Keep simple, print logs for demo
- Both can run from separate terminals
