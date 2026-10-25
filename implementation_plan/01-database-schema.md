# 01 - Database Schema

## Goal
Create SQLite schema storing: client names, IP addresses, TCP connection status, last heartbeat, response-time probe history, alerts, and event history.

## Schema

### clients
```sql
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    tcp_connected INTEGER DEFAULT 0,      -- 1 = persistent TCP connected
    status TEXT NOT NULL DEFAULT 'OFFLINE', -- ONLINE|WARNING|OFFLINE
    last_heartbeat TIMESTAMP,
    last_probe_at TIMESTAMP,
    rtt_ms REAL DEFAULT 0.0,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### response_time_probe_history
```sql
CREATE TABLE IF NOT EXISTS response_time_probe_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    probe_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rtt_ms REAL NOT NULL,
    success INTEGER DEFAULT 1,
    probe_type TEXT DEFAULT 'TCP',
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

### alerts
```sql
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    alert_type TEXT NOT NULL,            -- HEARTBEAT_MISS|PROBE_FAIL|TIMEOUT|STATUS_CHANGE
    message TEXT NOT NULL,
    severity TEXT DEFAULT 'MEDIUM',      -- LOW|MEDIUM|HIGH
    status_before TEXT,
    status_after TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged INTEGER DEFAULT 0,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

### event_history
```sql
CREATE TABLE IF NOT EXISTS event_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    event_type TEXT NOT NULL,            -- REGISTER|HEARTBEAT|PROBE|STATUS_CHANGE|ALERT|INFO
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

## Notes
- Use internal `clients.id` as FK
- Track `tcp_connected` separately from status
- Store full probe history for response times
- Keep exactly 3 statuses
- All timestamps stored as TEXT/DEFAULT CURRENT_TIMESTAMP (SQLite)
