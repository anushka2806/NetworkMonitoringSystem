import { Client, Alert, Event, ProbeHistory, StatusSummary } from '../types';

const API_BASE = 'http://127.0.0.1:8000';

const fetchWithNoCache = async (url: string) => {
  const res = await fetch(`${url}${url.includes('?') ? '&' : '?'}_t=${Date.now()}`, {
    cache: 'no-store',
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    }
  });
  return res.json();
};

export const fetchClients = async (): Promise<Client[]> => {
  return fetchWithNoCache(`${API_BASE}/clients`);
};

export const fetchAlerts = async (): Promise<Alert[]> => {
  return fetchWithNoCache(`${API_BASE}/alerts`);
};

export const fetchEvents = async (limit = 50): Promise<Event[]> => {
  return fetchWithNoCache(`${API_BASE}/events?limit=${limit}`);
};

export const fetchStatusSummary = async (): Promise<StatusSummary> => {
  return fetchWithNoCache(`${API_BASE}/status/summary`);
};

export const fetchProbeHistory = async (id: number, limit = 50): Promise<ProbeHistory[]> => {
  return fetchWithNoCache(`${API_BASE}/clients/${id}/probes?limit=${limit}`);
};
