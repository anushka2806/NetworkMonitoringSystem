# 03 - TCP Server Design (Registration + Persistent Connection + Probes)

## Goals
- Listen on TCP port 5000
- Accept client registration (client_name, ip_address)
- Maintain persistent TCP connections per client (track `tcp_connected`)
- Perform periodic request/response probes to measure RTT
- Store probe results in `response_time_probe_history` and update `last_probe_at`, `rtt_ms` in `clients`
- Non-blocking integration with FastAPI

## Registration
Client connects via TCP and sends registration payload:
```json
{"type":"REGISTER","client_name":"LAB-PC-1","ip_address":"192.168.1.100"}
```
Server:
1. Accept connection, assign to client record (create if not exists by name/IP or generate client_id)
2. Set `tcp_connected = 1`, update timestamps
3. Log REGISTER in `event_history`
4. Send ACK

## Persistent Connection
- Keep socket open in a managed connection map: `{client_id: socket, ...}`
- Handle disconnects (socket error) → set `tcp_connected = 0`, update, log INFO/STATUS_CHANGE context

## Periodic Probes (RTT Measurement)
- For each connected client, every PROBE_INTERVAL (10s), send probe request
- Example: `{"type":"PROBE","ts": <timestamp>}`
- Client responds: `{"type":"PROBE_RESP","ts": <original_ts>}` 
- Measure RTT = (recv_time - send_time) in ms
- On success: insert into `response_time_probe_history` (success=1, rtt_ms), update `clients.last_probe_at`, `clients.rtt_ms`, reset consecutive failures
- On timeout/failure: insert history (success=0), increment consecutive failures, do not update RTT to healthy value
- Store all probes (success/fail) in history as required

## Concurrency
- Use threading for each client connection or a thread pool
- Or asyncio with streams; but socket programming in threads is straightforward and easy to explain
- Must not block FastAPI event loop/HTTP requests

## Files
- `backend/app/services/tcp_server.py` - TCP server implementation
- Integration via FastAPI startup (thread/async task)
