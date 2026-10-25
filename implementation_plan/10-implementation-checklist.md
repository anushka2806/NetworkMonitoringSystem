# 10 - Implementation Checklist

## Setup
- [ ] Create implementation_plan folder with all .md files
- [ ] Verify folder structure matches
- [ ] Review schema, rules, ports

## Backend
- [ ] requirements.txt (fastapi, uvicorn)
- [ ] config.py with ports/thresholds
- [ ] db/schema.sql with revised schema
- [ ] db/session.py init and helpers
- [ ] services/tcp_server.py (register, persistent, probes, RTT)
- [ ] services/udp_server.py (heartbeats)
- [ ] services/monitor.py (rules, alerts, events)
- [ ] app/main.py (startup, CORS, routes)
- [ ] run.py

## Clients
- [ ] client/tcp_client.py
- [ ] client/udp_heartbeat.py

## Frontend
- [ ] package.json/tsconfig
- [ ] types/index.ts
- [ ] services/api.ts (real endpoints)
- [ ] components for table/cards/charts/alerts/events
- [ ] pages/Dashboard.tsx (real data)
- [ ] App.tsx, main.tsx, index.css

## Testing
- [ ] All test cases pass
- [ ] Non-blocking verified
- [ ] Exactly 3 statuses
- [ ] All required data stored
- [ ] Real data on dashboard

## Documentation
- [ ] Update agentlog.md with implementation steps
- [ ] Keep viva explainability in mind
