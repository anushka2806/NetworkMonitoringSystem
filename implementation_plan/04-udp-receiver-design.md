# 04 - UDP Receiver Design (Heartbeats)

## Goals
- Listen on UDP port 5001
- Receive periodic heartbeat messages from UDP clients
- Update `clients.last_heartbeat` timestamp
- Handle client identification
- Non-blocking, run concurrently with TCP server and API

## Heartbeat Payload
```json
{"type":"HEARTBEAT","client_name":"LAB-PC-1","ip_address":"192.168.1.100","ts": <epoch>}
```
Or use client_id if known. Match client by name/IP or registered client.

## Server Logic
1. Create UDP socket, bind to 0.0.0.0:5001
2. Receive datagrams in loop: `recvfrom()`
3. Parse JSON payload
4. Find matching client in DB (by client_name or ip_address; prefer registered client)
5. Update `last_heartbeat = CURRENT_TIMESTAMP`
6. Log HEARTBEAT in `event_history` (details)
7. Do not block - process quickly

## Concurrency
- Run in its own thread (blocking recvfrom is fine in thread)
- Or asyncio datagram protocol
- Must not block FastAPI

## Files
- `backend/app/services/udp_server.py`
- Integrated at FastAPI startup
