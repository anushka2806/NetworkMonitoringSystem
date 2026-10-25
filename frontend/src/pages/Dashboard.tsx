import { useEffect, useState } from 'react';
import { Client, Alert, Event, StatusSummary } from '../types';
import { fetchClients, fetchAlerts, fetchEvents, fetchStatusSummary } from '../services/api';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const Dashboard = () => {
  const [clients, setClients] = useState<Client[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [summary, setSummary] = useState<StatusSummary>({
    total_clients: 0,
    online: 0,
    warning: 0,
    offline: 0,
    total_alerts: 0,
    unacknowledged_alerts: 0
  });

  const loadData = async () => {
    try {
      const [clientsData, alertsData, eventsData, summaryData] = await Promise.all([
        fetchClients(),
        fetchAlerts(),
        fetchEvents(20),
        fetchStatusSummary()
      ]);
      setClients(clientsData);
      setAlerts(alertsData);
      setEvents(eventsData);
      setSummary(summaryData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const pieData = {
    labels: ['ONLINE', 'WARNING', 'OFFLINE'],
    datasets: [
      {
        data: [summary.online, summary.warning, summary.offline],
        backgroundColor: ['#2ecc71', '#f39c12', '#e74c3c'],
        borderWidth: 1,
      },
    ],
  };

  const barData = {
    labels: clients.map(c => c.client_name),
    datasets: [
      {
        label: 'RTT (ms)',
        data: clients.map(c => c.rtt_ms),
        backgroundColor: '#667eea',
      },
    ],
  };

  return (
    <div className="dashboard">
      <div className="header">
        <h1>Network Monitoring and Fault Detection System</h1>
        <p>Real-time monitoring with TCP Probes, UDP Heartbeats | ONLINE / WARNING / OFFLINE Status</p>
      </div>

      <div className="status-cards">
        <div className="status-card online">
          <h3>Online</h3>
          <div className="count">{summary.online}</div>
        </div>
        <div className="status-card warning">
          <h3>Warning</h3>
          <div className="count">{summary.warning}</div>
        </div>
        <div className="status-card offline">
          <h3>Offline</h3>
          <div className="count">{summary.offline}</div>
        </div>
        <div className="status-card alerts">
          <h3>Unacknowledged Alerts</h3>
          <div className="count">{summary.unacknowledged_alerts}</div>
        </div>
      </div>

      <div className="section">
        <h2>Client Status</h2>
        <table>
          <thead>
            <tr>
              <th>Client Name</th>
              <th>IP Address</th>
              <th>TCP Connected</th>
              <th>Status</th>
              <th>Last Heartbeat</th>
              <th>Last Probe</th>
              <th>RTT (ms)</th>
            </tr>
          </thead>
          <tbody>
            {clients.map(client => (
              <tr key={client.id}>
                <td>{client.client_name}</td>
                <td>{client.ip_address}</td>
                <td>{client.tcp_connected === 1 ? 'Yes' : 'No'}</td>
                <td><span className={`badge ${client.status.toLowerCase()}`}>{client.status}</span></td>
                <td>{client.last_heartbeat || 'N/A'}</td>
                <td>{client.last_probe_at || 'N/A'}</td>
                <td>{client.rtt_ms.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="charts-grid">
        <div className="section">
          <h2>Status Distribution</h2>
          <div className="chart-container">
            <Pie data={pieData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>
        <div className="section">
          <h2>RTT per Client</h2>
          <div className="chart-container">
            <Bar data={barData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>
      </div>

      <div className="section">
        <h2>Alerts</h2>
        <table>
          <thead>
            <tr>
              <th>Alert Type</th>
              <th>Message</th>
              <th>Status Change</th>
              <th>Severity</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {alerts.slice(0, 10).map(alert => (
              <tr key={alert.id}>
                <td>{alert.alert_type}</td>
                <td>{alert.message}</td>
                <td>{alert.status_before} → {alert.status_after}</td>
                <td><span className={`badge ${alert.severity.toLowerCase()}`}>{alert.severity}</span></td>
                <td>{alert.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="section">
        <h2>Recent Events</h2>
        <table>
          <thead>
            <tr>
              <th>Event Type</th>
              <th>Details</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {events.map(event => (
              <tr key={event.id}>
                <td>{event.event_type}</td>
                <td>{event.details}</td>
                <td>{event.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
