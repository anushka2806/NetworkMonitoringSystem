# Frontend Design (React + TypeScript + Chart.js)

## Overview

The frontend is a single-page web application built with React.js and TypeScript. It provides a clean dashboard to visualize network monitoring data from the FastAPI backend.

## Tech Stack (Frontend)
- **React.js** - UI framework
- **TypeScript** - Type safety
- **HTML5 & CSS3** - Markup and styling
- **Chart.js** - Data visualization (with react-chartjs-2 wrapper conceptually)
- **Fetch API / Axios** - HTTP requests to backend

## Project Structure

```text
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── StatusCard.tsx      # Summary cards (Total/Online/Offline/Alerts)
│   │   ├── ClientTable.tsx     # Table showing all clients
│   │   ├── AlertList.tsx       # List of alerts
│   │   ├── EventLog.tsx        # Recent events log
│   │   └── Charts.tsx          # Chart.js visualizations
│   ├── pages/
│   │   └── Dashboard.tsx       # Main dashboard page
│   ├── services/
│   │   └── api.ts              # API calls to FastAPI
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces
│   ├── App.tsx                 # Root component
│   ├── index.css               # Global styles
│   └── main.tsx                # Entry point
├── package.json
├── tsconfig.json
└── index.html
```

## TypeScript Types (`src/types/index.ts`)

Define interfaces matching backend API responses:

```typescript
export interface Client {
  id: number;
  client_id: string;
  hostname: string;
  ip_address: string;
  port: number;
  status: 'ONLINE' | 'OFFLINE';
  last_seen: string;
  registered_at: string;
  rtt_ms: number;
  notes: string | null;
}

export interface Alert {
  id: number;
  client_id: string;
  alert_type: string;
  message: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH';
  timestamp: string;
  acknowledged: number;
}

export interface Event {
  id: number;
  event_type: string;
  client_id: string | null;
  details: string;
  timestamp: string;
}

export interface StatusSummary {
  total_clients: number;
  online_clients: number;
  offline_clients: number;
  total_alerts: number;
  unacknowledged_alerts: number;
  total_events: number;
  last_updated: string;
}
```

## API Service (`src/services/api.ts`)

Centralized API calls:

```typescript
const API_BASE = 'http://localhost:8000';

export const fetchClients = async (): Promise<Client[]> => {
  const res = await fetch(`${API_BASE}/clients`);
  return res.json();
};

export const fetchAlerts = async (): Promise<Alert[]> => {
  const res = await fetch(`${API_BASE}/alerts`);
  return res.json();
};

export const fetchEvents = async (limit = 50): Promise<Event[]> => {
  const res = await fetch(`${API_BASE}/events?limit=${limit}`);
  return res.json();
};

export const fetchStatus = async (): Promise<StatusSummary> => {
  const res = await fetch(`${API_BASE}/status`);
  return res.json();
};

export const acknowledgeAlert = async (alertId: number): Promise<any> => {
  const res = await fetch(`${API_BASE}/alerts/${alertId}/ack`, { method: 'POST' });
  return res.json();
};
```

## Components

### 1. StatusCard.tsx
Displays summary statistics in card format.
- Props: title, value, icon/color
- Shows: Total Clients, Online, Offline, Unacknowledged Alerts

### 2. ClientTable.tsx
Table of all registered clients.
- Columns: Client ID, Hostname, IP Address, Status, Last Seen, RTT (ms)
- Status displayed with color badges (Green for ONLINE, Red for OFFLINE)
- Sortable by default

### 3. AlertList.tsx
List of recent alerts.
- Shows alert type, message, severity, timestamp, client_id
- Button to acknowledge alert
- Different styling for severity levels

### 4. EventLog.tsx
Chronological event log.
- Shows event_type, client_id, details, timestamp
- Limited to recent events

### 5. Charts.tsx
Chart.js visualizations.

**Chart 1: Client Status Distribution (Pie/Doughnut)**
- Data: Online vs Offline count
- Colors: Green, Red

**Chart 2: RTT Overview (Bar Chart)**
- Data: RTT values per client
- X-axis: Client IDs, Y-axis: RTT (ms)

## Dashboard Layout (`src/pages/Dashboard.tsx`)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Network Monitoring Dashboard                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐
│  Total  │ │  Online │ │ Offline │ │ Unack Alerts│  (Status Cards)
└─────────┘ └─────────┘ └─────────┘ └─────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────┐
│      Client Status Table        │ │   Status Distribution Chart │
└─────────────────────────────────┘ └─────────────────────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────┐
│         Alerts Panel            │ │      RTT Chart              │
└─────────────────────────────────┘ ┌─────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Recent Events Log                        │
└─────────────────────────────────────────────────────────────────┘
```

## Styling (`index.css`)

- Clean, minimal design suitable for college project
- CSS Grid/Flexbox for layout
- Color scheme:
  - Online: `#2ecc71` (Green)
  - Offline: `#e74c3c` (Red)
  - Alerts: `#f39c12` (Orange)
  - Info: `#3498db` (Blue)
- Responsive layout where possible

## Data Flow in Frontend
1. Dashboard mounts → useEffect runs
2. Fetch all required data simultaneously (Promise.all)
3. Store in component state (useState)
5. Auto-refresh every 10-30 seconds (optional but nice for demo)
6. Update UI reactively

## Chart.js Setup (Conceptual)
- Register required elements (ArcElement, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend)
- Use react-chartjs-2 components: Pie, Bar, Doughnut
- Pass data and options as props

## Notes
- Keep components functional with hooks (useState, useEffect)
- TypeScript strictness helps catch errors
- Simple CSS without heavy UI libraries (keeps project lightweight)
- Dashboard refreshes data periodically to show live status changes
- Chart.js provides clear visual representation for viva demonstration
