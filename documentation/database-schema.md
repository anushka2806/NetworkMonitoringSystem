# Database Schema (SQLite)

## Overview

The system uses SQLite for persistent storage. All tables are defined in `backend/app/db/schema.sql`. The database file will be created on first run (e.g., `monitor.db` in backend directory or configured path).

## Tables

### 1. `clients`
Stores registered client information and current monitoring status.

| Column | Type | Constraints | Description |
| :-- | :-- | :-- | :-- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique internal ID |
| `client_id` | TEXT | UNIQUE NOT NULL | Unique identifier for client (e.g., hostname or custom ID) |
| `hostname` | TEXT |  | Client hostname |
| `ip_address` | TEXT |  | Client IP address |
| `port` | INTEGER |  | TCP/communication port if applicable |
| `status` | TEXT | NOT NULL DEFAULT 'OFFLINE' | Current status: 'ONLINE' or 'OFFLINE' |
| `last_seen` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last heartbeat/communication timestamp (UTC or local) |
| `registered_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |
| `rtt_ms` | REAL | DEFAULT 0.0 | Last measured Round Trip Time in milliseconds |
| `notes` | TEXT |  | Optional notes |

**Indexes:** Consider index on `client_id`, `status`, `last_seen` for faster lookups.

### 2. `probes`
Configuration for monitoring probes (extensible for future enhancements).

| Column | Type | Constraints | Description |
| :-- | :-- | :-- | :-- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique probe ID |
| `name` | TEXT | NOT NULL | Probe name |
| `target` | TEXT | NOT NULL | Target host/IP to monitor |
| `type` | TEXT | NOT NULL | Probe type: 'TCP' or 'UDP' |
| `interval_sec` | INTEGER | DEFAULT 10 | Check interval in seconds |
| `enabled` | INTEGER | DEFAULT 1 | 1 = enabled, 0 = disabled |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

### 3. `alerts`
Stores generated fault alerts when clients go offline or faults detected.

| Column | Type | Constraints | Description |
| :-- | :-- | :-- | :-- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique alert ID |
| `client_id` | TEXT | NOT NULL | Reference to client_id |
| `alert_type` | TEXT | NOT NULL | Type of alert: 'FAULT', 'TIMEOUT', 'CONNECTION_LOST' |
| `message` | TEXT | NOT NULL | Alert message description |
| `severity` | TEXT | DEFAULT 'MEDIUM' | Severity: 'LOW', 'MEDIUM', 'HIGH' |
| `timestamp` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Alert generation timestamp |
| `acknowledged` | INTEGER | DEFAULT 0 | 0 = not acknowledged, 1 = acknowledged |

**Foreign Key Consideration:** Can reference `clients(client_id)` but SQLite foreign keys need to be enabled; for simplicity in mini-project we can just store client_id.

### 4. `events`
System event log for audit trail and debugging.

| Column | Type | Constraints | Description |
| :-- | :-- | :-- | :-- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique event ID |
| `event_type` | TEXT | NOT NULL | Event type: 'REGISTER', 'HEARTBEAT', 'STATUS_CHANGE', 'ALERT', 'INFO' |
| `client_id` | TEXT |  | Related client_id (if applicable) |
| `details` | TEXT |  | Detailed event information (JSON or plain text) |
| `timestamp` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Event timestamp |

## Schema SQL (Reference)

```sql
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT UNIQUE NOT NULL,
    hostname TEXT,
    ip_address TEXT,
    port INTEGER,
    status TEXT NOT NULL DEFAULT 'OFFLINE',
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rtt_ms REAL DEFAULT 0.0,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS probes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target TEXT NOT NULL,
    type TEXT NOT NULL,
    interval_sec INTEGER DEFAULT 10,
    enabled INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    message TEXT NOT NULL,
    severity TEXT DEFAULT 'MEDIUM',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    client_id TEXT,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Sample Data (For Understanding)

**clients:**
| client_id | hostname | ip_address | status | last_seen | rtt_ms |
| :-- | :-- | :-- | :-- | :-- | :-- |
| client-01 | LAB-PC-1 | 192.168.1.100 | ONLINE | 2026-10-24 10:30:45 | 15.3 |
| client-02 | LAB-PC-2 | 192.168.1.101 | OFFLINE | 2026-10-24 10:25:10 | 0.0 |

**alerts:**
| client_id | alert_type | message | severity | timestamp |
| :-- | :-- | :-- | :-- | :-- |
| client-02 | FAULT | Client client-02 is offline - no heartbeat received | HIGH | 2026-10-24 10:26:00 |

**events:**
| event_type | client_id | details | timestamp |
| :-- | :-- | :-- | :-- |
| REGISTER | client-01 | Client registered via TCP | 2026-10-24 10:20:00 |
| HEARTBEAT | client-01 | UDP heartbeat received | 2026-10-24 10:30:45 |
| STATUS_CHANGE | client-02 | Status changed from ONLINE to OFFLINE | 2026-10-24 10:26:00 |
| ALERT | client-02 | Fault alert generated | 2026-10-24 10:26:00 |

## Notes

- Timestamps use SQLite's `CURRENT_TIMESTAMP` (UTC by default in many setups) - for local demo either is fine
- `last_seen` is critical for heartbeat timeout calculation
- Status values are constrained to ONLINE/OFFLINE conceptually
- All tables use AUTOINCREMENT primary keys for easy reference
