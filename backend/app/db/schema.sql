-- Network Monitoring and Fault Detection System - Database Schema

-- Clients table: store client names, IP addresses, TCP connection status, last heartbeat
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    tcp_connected INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'OFFLINE',
    last_heartbeat TIMESTAMP,
    last_probe_at TIMESTAMP,
    rtt_ms REAL DEFAULT 0.0,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Response time probe history: store RTT/probe history
CREATE TABLE IF NOT EXISTS response_time_probe_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    probe_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rtt_ms REAL NOT NULL,
    success INTEGER DEFAULT 1,
    probe_type TEXT DEFAULT 'TCP',
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Alerts table: store generated alerts
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    alert_type TEXT NOT NULL,
    message TEXT NOT NULL,
    severity TEXT DEFAULT 'MEDIUM',
    status_before TEXT,
    status_after TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged INTEGER DEFAULT 0,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Event history table: store all system events
CREATE TABLE IF NOT EXISTS event_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    event_type TEXT NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
