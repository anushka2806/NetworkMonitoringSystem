# 00 - Overview

## Project
Network Monitoring and Fault Detection System (College Computer Networks Mini-Project)

## Objectives
- Register clients (name/IP) over TCP with persistent connections
- Monitor TCP connectivity and perform periodic request/response probes to measure RTT
- Receive periodic UDP heartbeats
- Track last heartbeat and probe history in SQLite
- Use exactly three statuses: ONLINE, WARNING, OFFLINE with clearly defined conditions
- Generate alerts and maintain event history
- Expose data via FastAPI (non-blocking) and display on React dashboard with real backend data
- Keep implementation simple enough for viva explanation

## Technology Stack (Unchanged)
- Python + FastAPI
- TCP socket programming
- UDP socket programming
- SQLite
- React.js + TypeScript
- HTML, CSS, Chart.js

## Key Requirements
1. SQLite must store client names, IP addresses, TCP connection status, last heartbeat, response-time probe history, alerts, and event history.
2. TCP clients must register and maintain a persistent connection. Implement periodic request/response probes to measure RTT.
3. UDP clients must send periodic heartbeat messages. Mark WARNING or OFFLINE when heartbeats or TCP probes fail using thresholds.
4. Exactly three statuses: ONLINE, WARNING, OFFLINE. Conditions defined.
5. FastAPI must run TCP server, UDP receiver, and monitoring logic without blocking HTTP requests.
6. React dashboard must use real backend API data (no mock data).

## Ports
- TCP: 5000 (registration + persistent + probes)
- UDP: 5001 (heartbeats)
- FastAPI: 8000
- React dev: 5173/3000 (configurable)

## Intervals/Thresholds (Defaults)
- Heartbeat interval (client): 5s
- Heartbeat WARNING: >10s since last_heartbeat
- Heartbeat OFFLINE: >15s since last_heartbeat
- Probe interval: 10s
- Probe failures → WARNING at >=2 consecutive, OFFLINE at >=4 consecutive
- Monitor check interval: 2-3s
