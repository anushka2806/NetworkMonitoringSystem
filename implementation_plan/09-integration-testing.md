# 09 - Integration Testing

## Setup
- Backend: run from backend/ with uvicorn (starts TCP/UDP/monitor)
- Clients: run tcp_client.py and udp_heartbeat.py
- Frontend: npm run dev pointing to API

## Test Cases

### DB/Schema
- [ ] All 4 tables created with correct columns
- [ ] FK relationships work
- [ ] Fields match requirements (client names, IP, tcp_connected, last heartbeat, probe history, alerts, event history)

### TCP Registration & Persistent
- [ ] Client registers over TCP → record created
- [ ] tcp_connected becomes 1
- [ ] Persistent connection maintained
- [ ] Event REGISTER logged

### Probes & RTT
- [ ] Server sends probes every 10s
- [ ] Client responds → RTT measured
- [ ] Stored in response_time_probe_history (success=1)
- [ ] clients.rtt_ms and last_probe_at updated
- [ ] Failed probes recorded as success=0

### UDP Heartbeats
- [ ] Heartbeats received every 5s
- [ ] last_heartbeat updated
- [ ] HEARTBEAT event logged

### Status Rules
- [ ] All healthy → ONLINE
- [ ] Miss heartbeat (>10s) but <15s or probe issues start → WARNING
- [ ] Miss heartbeat (>15s) or >=4 probe failures or tcp_connected lost → OFFLINE
- [ ] Recovery works both ways
- [ ] Only transitions generate alerts

### Non-blocking
- [ ] API responds while TCP/UDP/monitor running
- [ ] No blocking of HTTP requests

### Frontend Real Data
- [ ] Dashboard shows real data from API
- [ ] Badges for ONLINE/WARNING/OFFLINE
- [ ] Probe history visible
- [ ] Alerts show status_before→status_after
- [ ] No mock data

### End-to-End Demo
1. Start backend
2. Start tcp_client
3. Start udp_heartbeat
4. Open dashboard - ONLINE
5. Stop heartbeat → WARNING then OFFLINE with alert
6. Restart heartbeat → back to ONLINE
7. Stop TCP client → tcp_connected 0 affects status
8. Show probe history and RTT
