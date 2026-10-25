# Implementation Guide

## Overview

This guide provides a step-by-step approach to implement the Network Monitoring and Fault Detection System. Follow the order below for smooth integration.

## Prerequisites
- Python 3.8+ installed
- Node.js and npm installed
- Basic knowledge of sockets, FastAPI, React, SQLite
- Terminal/Command Prompt access

## Implementation Order

### Step 1: Database Setup
**Goal:** Create SQLite schema and database session

**Files to create/modify:**
- `backend/app/db/schema.sql` - Table definitions
- `backend/app/db/session.py` - DB connection and helpers
- `backend/app/db/__init__.py`

**Tasks:**
1. Write schema.sql with all 4 tables (clients, probes, alerts, events)
2. Create session.py with functions to connect, initialize DB, execute queries
3. Test DB creation

**Checkpoint:** Database file created with all tables

---

### Step 2: Configuration
**Goal:** Centralize configuration

**Files:**
- `backend/app/config.py`

**Tasks:**
1. Define TCP_SERVER_HOST, TCP_SERVER_PORT
2. Define UDP_SERVER_HOST, UDP_SERVER_PORT
3. Define HEARTBEAT_INTERVAL, HEARTBEAT_TIMEOUT
4. Define DATABASE_PATH
5. Define API_HOST, API_PORT

**Checkpoint:** Config accessible across modules

---

### Step 3: TCP Server (Socket Programming)
**Goal:** Handle client registration via TCP

**Files:**
- `backend/app/services/tcp_server.py`
- `backend/app/services/__init__.py`

**Tasks:**
1. Create TCP socket, bind, listen
2. Accept client connections
3. Receive registration data (parse JSON)
4. Insert/update client in DB, set status ONLINE
5. Log registration event
6. Send acknowledgment
7. Handle multiple clients (threading)

**Key Concepts:** SOCK_STREAM, bind(), listen(), accept(), recv(), send()

**Checkpoint:** Client can register via TCP and appears in DB

---

### Step 4: UDP Server (Socket Programming)
**Goal:** Handle heartbeats via UDP

**Files:**
- `backend/app/services/udp_server.py`

**Tasks:**
1. Create UDP socket, bind
2. Listen for datagrams
3. Parse heartbeat payload (client_id, timestamp)
4. Update clients.last_seen for matching client
5. Update status to ONLINE if was OFFLINE
6. Log heartbeat event
7. Run in background

**Key Concepts:** SOCK_DGRAM, recvfrom(), no connection needed

**Checkpoint:** UDP heartbeats update last_seen in DB

---

### Step 5: Monitor Service (Fault Detection)
**Goal:** Detect offline clients and generate alerts

**Files:**
- `backend/app/services/monitor.py`

**Tasks:**
1. Create background monitoring loop
2. Periodically fetch all clients from DB
3. For each client calculate time since last_seen
4. If delta > HEARTBEAT_TIMEOUT and status == ONLINE:
   - Set status to OFFLINE
   - Create alert in alerts table
   - Log STATUS_CHANGE and ALERT events
5. Handle recovery (OFFLINE -> ONLINE)
6. Run as asyncio task or thread

**Checkpoint:** Stopping heartbeat causes client to go offline with alert

---

### Step 6: FastAPI Backend
**Goal:** Expose REST API

**Files:**
- `backend/app/main.py`
- `backend/app/routers/*.py` (or inline routes)
- `backend/app/models/__init__.py`
- `backend/run.py`
- `backend/requirements.txt`

**Tasks:**
1. Create FastAPI app instance
2. Add CORS middleware
3. Initialize DB on startup
4. Start TCP server, UDP server, Monitor in background
5. Implement routes: /clients, /clients/{id}, /alerts, /events, /status, /health
6. Create run.py to start uvicorn
7. Add requirements.txt (fastapi, uvicorn)

**Checkpoint:** API accessible at http://localhost:8000, returns data

---

### Step 7: Client Agents
**Goal:** Create client programs to test

**Files:**
- `client/tcp_client.py`
- `client/udp_heartbeat.py`

**Tasks:**
1. **tcp_client.py:**
   - Connect to TCP server
   - Send registration JSON
   - Receive acknowledgment
   - Keep connection alive or exit
   
2. **udp_heartbeat.py:**
   - Send UDP packets to UDP server every HEARTBEAT_INTERVAL seconds
   - Include client_id and timestamp
   - Run in loop

**Checkpoint:** Can simulate clients from separate terminals

---

### Step 8: Frontend Setup (React + TypeScript)
**Goal:** Create dashboard UI

**Files:**
- `frontend/package.json`
- `frontend/tsconfig.json`
- `frontend/index.html`
- `frontend/src/main.tsx`, `App.tsx`
- `frontend/src/types/index.ts`
- `frontend/src/services/api.ts`
- `frontend/src/components/*.tsx`
- `frontend/src/pages/Dashboard.tsx`

**Tasks:**
1. Setup React + TypeScript project structure
2. Define types matching API
3. Create API service
4. Build components (StatusCard, ClientTable, AlertList, EventLog, Charts)
5. Create Dashboard page with layout
6. Add CSS styling
7. Integrate Chart.js for visualizations
8. Add data fetching with useEffect
9. Optional: Auto-refresh

**Checkpoint:** Dashboard displays clients, alerts, events, charts

---

### Step 9: Integration & Testing
**Goal:** Run entire system together

**Tasks:**
1. Start backend: `python run.py` or `uvicorn app.main:app`
2. Start client agents in separate terminals
3. Open frontend in browser
4. Verify registration, heartbeats, fault detection
5. Check dashboard updates

**Checkpoint:** End-to-end working system

## Tips for Implementation
- Start simple, test incrementally
- Use print statements for debugging sockets
- Test TCP and UDP separately first
- Keep JSON payloads consistent
- Use threading for concurrent socket handling
- SQLite is file-based - easy to inspect
- Chart.js documentation helps for quick charts
- Follow the exact tech stack - no substitutions

## Common Pitfalls to Avoid
- Mixing up TCP/UDP ports
- Not updating last_seen correctly
- Timeout calculation errors
- CORS issues between frontend/backend
- Forgetting to start background tasks
- SQLite locks with multiple threads (use proper connection handling)

## Verification Checklist
- [ ] DB schema created correctly
- [ ] TCP server accepts registrations
- [ ] UDP server receives heartbeats
- [ ] Monitor detects offline clients
- [ ] Alerts generated on fault
- [ tags]
- [ ] Events logged properly
- [ ] FastAPI endpoints working
- [ ] Client agents functional
- [ ] Dashboard displays all data
- [ ] Charts render correctly
- [ ] Both TCP and UDP demonstrated
- [ ] RTT measurement visible
- [ ] Online/Offline status accurate
