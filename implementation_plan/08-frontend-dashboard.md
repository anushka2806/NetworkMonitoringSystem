# 08 - Frontend Dashboard (Real Data, No Mock)

## Goals
Build React + TypeScript dashboard using real backend API data. Show exactly three statuses with clear badges.

## Types (match schema)
```typescript
export interface Client {
  id: number;
  client_name: string;
  ip_address: string;
  tcp_connected: number;
  status: 'ONLINE' | 'WARNING' | 'OFFLINE';
  last_heartbeat: string | null;
  last_probe_at: string | null;
  rtt_ms: number;
  registered_at: string;
  updated_at: string;
}

export interface Alert { ... status_before, status_after ... }
export interface Event { ... event_history fields ... }
export interface ProbeHistory { ... response_time_probe_history ... }
```

## Components
- `StatusSummary.tsx` - cards for ONLINE/WARNING/OFFLINE counts
- `ClientTable.tsx` - table with client_name, ip_address, tcp_connected, status (badge), last_heartbeat, last_probe_at, rtt_ms
- `AlertList.tsx` - alerts with status_before→status_after
- `EventLog.tsx` - event_history
- `ProbeHistoryModal.tsx` or section - show probe history per client
- `Charts.tsx` - status distribution (pie) and RTT (bar)

## Pages
- `Dashboard.tsx` - layout, fetch all data on mount, auto-refresh every few seconds

## API Service
`src/services/api.ts` hits `http://localhost:8000` endpoints returning real data.

## Styling
Color badges:
- ONLINE: green (#2ecc71)
- WARNING: orange (#f39c12)
- OFFLINE: red (#e74c3c)

## Notes
- No hardcoded/mock arrays
- Fetch from real endpoints
- Display all required fields
- Simple and viva-friendly
