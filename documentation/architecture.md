# System Architecture

## Overview

The Network Monitoring and Fault Detection System follows a client-server architecture with three primary communication channels: REST API (for dashboard), TCP (for client registration and monitoring), and UDP (for heartbeat-based liveness checks).

## Architectural Components

### 1. Client Agents
- **tcp_client.py** - Establishes TCP connection to server, sends registration payload, maintains connection
- **udp_heartbeat.py** - Sends periodic UDP heartbeat packets to server to indicate liveness

### 2. Monitoring Server (Backend)
The backend consists of multiple coordinated components:

#### TCP Server (`app/services/tcp_server.py`)
- Listens for incoming TCP connections on configured port
- Handles client registration (accepts client info: hostname/IP/ID)
- Tracks active TCP connections
- Can measure connection establishment time / response characteristics
- Logs registration events

#### UDP Server (`app/services/udp_server.py`)
- Listens for incoming UDP datagrams on configured port
- Receives heartbeat messages from clients
- Updates `last_seen` timestamp in database for corresponding client
- Handles heartbeat processing asynchronously

#### Monitor Service (`app/services/monitor.py`)
- Core fault detection logic
- Periodically checks all registered clients
- Compares current time with `last_seen` timestamp
- If (current_time - last_seen) > timeout threshold → mark as OFFLINE
- If client was ONLINE and becomes OFFLINE → generate fault alert
- Log status change events
- Calculate/track RTT where applicable

#### Database Layer (`app/db/`)
- **schema.sql** - Table definitions for clients, probes, alerts, events
- **session.py** - SQLite connection management, helper functions for CRUD operations

#### FastAPI Application (`app/`)
- **main.py** - Application entry point, CORS setup, route registration, server startup hooks
- **routers/** - REST endpoint definitions
- **models/** - Data models/schemas (Pydantic models for request/response validation)
- **config.py** - Configuration (ports, timeouts, DB path)
- **utils/** - Helper utilities

### 3. Database (SQLite)
Stores all persistent data:
- `clients` - Registered client information and status
- `probes` - Monitoring probe configurations
- `alerts` - Generated fault alerts
- `events` - System/event logs

### 4. Frontend Dashboard (React + TypeScript)
- **Dashboard.tsx** - Main dashboard page
- **components/** - Reusable UI components (ClientTable, AlertList, StatusCard, Charts)
- **services/api.ts** - API client for FastAPI backend
- **types/** - TypeScript interfaces matching backend models
- **Chart.js** - Visualizations for status distribution, RTT trends

## Data Flow

### Flow 1: Client Registration (TCP)
```
1. Client starts tcp_client.py
2. Opens TCP connection to server:port
3. Sends registration data (client_id, hostname, ip)
4. TCP Server accepts connection, parses data
5. Server checks if client exists in DB; if not, inserts new record with status=ONLINE
6. Server logs registration event in 'events' table
7. Server may acknowledge registration
8. Connection can be kept alive or closed based on design
```

### Flow 2: Heartbeat Monitoring (UDP)
```
1. Client starts udp_heartbeat.py (after/during registration)
2. Sends UDP packet with heartbeat payload (client_id, timestamp) every T seconds
3. UDP Server receives packet
4. Looks up client in DB by client_id
5. Updates clients.last_seen = current_timestamp
6. (Optionally updates status to ONLINE if previously offline)
7. No connection establishment - UDP is connectionless
```

### Flow 3: Fault Detection
```
1. Monitor service runs in background (async task/thread)
2. Every check_interval seconds, queries all clients
3. For each client: if (now - last_seen) > HEARTBEAT_TIMEOUT
   - If current status is ONLINE:
     * Set status = OFFLINE
     * Create alert in 'alerts' table (type=FAULT, message)
     * Log status_change event in 'events' table
   - If already OFFLINE: do nothing or update alert
4. Monitor continues checking
```

### Flow 4: Dashboard Display
```
1. User opens React app in browser
2. App loads Dashboard component
3. Dashboard calls api.ts functions to fetch /clients, /alerts, /events, /status
4. FastAPI queries SQLite and returns JSON
5. Dashboard renders tables, cards and Chart.js graphs
6. Can auto-refresh periodically for near real-time view
```

## Design Principles

- **Simplicity:** Easy to understand and explain in viva
- **Separation of Concerns:** TCP/UDP/monitor/API/frontend clearly separated
- **Educational Focus:** Demonstrates both connection-oriented (TCP) and connectionless (UDP) protocols
- **Minimal Dependencies:** Uses built-in Python socket, sqlite3; minimal npm packages
- **Extensible:** Structure allows easy addition of features

## Network Protocols Usage

| Protocol | Use Case | Rationale |
| :-- | :-- | :-- |
| **TCP** | Client Registration & Connection Monitoring | Reliable, connection-oriented. Ensures registration is received. Good for demonstrating 3-way handshake concept. |
| **UDP** | Heartbeat Messages | Lightweight, connectionless, low overhead. Heartbeats are small and don't need guaranteed delivery - if a heartbeat is lost occasionally, next one will come; persistent loss indicates fault. |
| **HTTP/REST** | API Communication | Standard for web apps, easy integration with React |

## Concurrency Model

- **TCP Server:** Can use threading or asyncio for handling multiple clients
- **UDP Server:** Typically single socket, can process packets as they arrive
- **Monitor:** Background task (asyncio task in FastAPI or separate thread)
- **FastAPI:** Async ASGI server (Uvicorn)

All designed to run concurrently within the backend process.
