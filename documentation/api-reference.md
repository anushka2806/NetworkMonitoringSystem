# API Reference

## Overview

The FastAPI backend exposes REST endpoints for the React dashboard to consume. All endpoints return JSON responses. CORS is enabled for frontend communication.

**Base URL (Development):** `http://localhost:8000`  
**API Prefix:** Can be used as-is or with `/api` prefix (flexible based on setup)

## Endpoints

### 1. Get All Clients
Retrieves all registered clients with their status, last seen time and RTT.

- **URL:** `/clients`
- **Method:** `GET`
- **Description:** List all clients in the system
- **Request Body:** None
- **Response:** `200 OK`

```json
[
  {
    "id": 1,
    "client_id": "client-01",
    "hostname": "LAB-PC-1",
    "ip_address": "192.168.1.100",
    "port": 5000,
    "status": "ONLINE",
    "last_seen": "2026-10-24T10:30:45",
    "registered_at": "2026-10-24T10:20:00",
    "rtt_ms": 15.3,
    "notes": null
  },
  {
    "id": 2,
    "client_id": "client-02",
    "hostname": "LAB-PC-2",
    "ip_address": "192.168.1.101",
    "port": 5000,
    "status": "OFFLINE",
    "last_seen": "2026-10-24T10:25:10",
    "registered_at": "2026-10-24T10:21:00",
    "rtt_ms": 0.0,
    "notes": null
  }
]
```

### 2. Get Client by ID
Retrieves details of a specific client.

- **URL:** `/clients/{client_id}`
- **Method:** `GET`
- **Description:** Get single client details
- **Path Parameters:** `client_id` (string) - Client identifier
- **Response:** `200 OK` or `404 Not Found`

```json
{
  "id": 1,
  "client_id": "client-01",
  "hostname": "LAB-PC-1",
  "ip_address": "192.168.1.100",
  "port": 5000,
  "status": "ONLINE",
  "last_seen": "2026-10-24T10:30:45",
  "registered_at": "2026-10-24T10:20:00",
  "rtt_ms": 15.3,
  "notes": null
}
```

### 3. Get System Status Summary
Overview of monitoring system status.

- **URL:** `/status`
- **Method:** `GET`
- **Description:** Aggregated statistics
- **Response:** `200 OK`

```json
{
  "total_clients": 2,
  "online_clients": 1,
  "offline_clients": 1,
  "total_alerts": 1,
  "unacknowledged_alerts": 1,
  "total_events": 10,
  "last_updated": "2026-10-24T10:31:00"
}
```

### 4. Get All Alerts
Retrieves all fault alerts.

- **URL:** `/alerts`
- **Method:** `GET`
- **Description:** List all alerts (newest first)
- **Query Parameters (optional):** 
  - `acknowledged` (bool) - Filter by acknowledgment status
  - `limit` (int) - Limit number of results
- **Response:** `200 OK`

```json
[
  {
    "id": 1,
    "client_id": "client-02",
    "alert_type": "FAULT",
    "message": "Client client-02 is offline - no heartbeat received",
    "severity": "HIGH",
    "timestamp": "2026-10-24T10:26:00",
    "acknowledged": 0
  }
]
```

### 5. Acknowledge Alert
Mark an alert as acknowledged.

- **URL:** `/alerts/{alert_id}/ack`
- **Method:** `POST` or `PUT`
- **Description:** Acknowledge a specific alert
- **Path Parameters:** `alert_id` (int)
- **Response:** `200 OK` or `404 Not Found`

```json
{
  "message": "Alert acknowledged successfully",
  "alert_id": 1
}
```

### 6. Get All Events
Retrieves system event logs.

- **URL:** `/events`
- **Method:** `GET`
- **Description:** Event history (newest first)
- **Query Parameters (optional):**
  - `limit` (int) - Number of events to return (default: 50)
  - `event_type` (string) - Filter by event type
- **Response:** `200 OK`

```json
[
  {
    "id": 10,
    "event_type": "HEARTBEAT",
    "client_id": "client-01",
    "details": "UDP heartbeat received",
    "timestamp": "2026-10-24T10:30:45"
  },
  {
    "id": 9,
    "event_type": "STATUS_CHANGE",
    "client_id": "client-02",
    "details": "Status changed from ONLINE to OFFLINE",
    "timestamp": "2026-10-24T10:26:00"
  }
]
```

### 7. Health Check (Optional but useful)
Check if API is running.

- **URL:** `/health`
- **Method:** `GET`
- **Description:** API health status
- **Response:** `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "2026-10-24T10:31:00"
}
```

## Error Responses

| Status Code | Meaning | Example |
| :-- | :-- | :-- |
| `404` | Not Found | Client/Alert not found |
| `500` | Internal Server Error | Database error |
| `422` | Validation Error | Invalid request data (FastAPI automatic) |

## CORS Configuration

For React frontend running on different port (e.g., `http://localhost:5173` or `http://localhost:3000`), CORS must be enabled:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Notes

- All timestamps in ISO 8601 format
- Endpoints are RESTful and simple for educational purposes
- No authentication required (mini-project scope)
- Data comes directly from SQLite database
- Frontend will poll these endpoints or fetch on demand
