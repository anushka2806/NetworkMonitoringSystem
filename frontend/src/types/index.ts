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

export interface Alert {
  id: number;
  client_id: number;
  alert_type: string;
  message: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH';
  status_before: string | null;
  status_after: string | null;
  timestamp: string;
  acknowledged: number;
}

export interface Event {
  id: number;
  client_id: number | null;
  event_type: string;
  details: string | null;
  timestamp: string;
}

export interface ProbeHistory {
  id: number;
  client_id: number;
  probe_at: string;
  rtt_ms: number;
  success: number;
  probe_type: string;
}

export interface StatusSummary {
  total_clients: number;
  online: number;
  warning: number;
  offline: number;
  total_alerts: number;
  unacknowledged_alerts: number;
}
