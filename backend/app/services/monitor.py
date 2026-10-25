import time
import threading
from datetime import datetime
from backend.app.db.session import fetch_all, fetch_one, execute_query
from backend.app import config

def count_consecutive_failures(client_id):
    """Count consecutive failed probes from most recent probes"""
    probes = fetch_all(
        "SELECT success FROM response_time_probe_history WHERE client_id = ? ORDER BY probe_at DESC LIMIT 20",
        (client_id,)
    )
    if not probes:
        return 0
    count = 0
    for probe in probes:
        if probe['success'] == 0:
            count += 1
        else:
            break
    return count

def start_monitor():
    """Start monitoring service in background thread"""
    print(f"[MONITOR] Service starting (check interval: {config.MONITOR_CHECK_INTERVAL}s)")
    while True:
        try:
            evaluate_clients()
        except Exception as e:
            print(f"[MONITOR] Error: {e}")
        time.sleep(config.MONITOR_CHECK_INTERVAL)

def evaluate_clients():
    """Evaluate all clients and update status based on rules"""
    clients = fetch_all("SELECT * FROM clients")
    # DB timestamps are stored in local time via datetime('now','localtime')
    now = datetime.now()
    
    for client in clients:
        client_id = client['id']
        current_status = client['status']
        tcp_connected = client['tcp_connected']
        
        # Calculate heartbeat age
        hb_age = float('inf')
        if client['last_heartbeat']:
            try:
                last_hb_str = str(client['last_heartbeat'])
                # Try different formats
                try:
                    last_hb = datetime.strptime(last_hb_str, '%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        last_hb = datetime.fromisoformat(last_hb_str.replace('Z', ''))
                    except:
                        hb_age = float('inf')
                    else:
                        hb_age = (now - last_hb).total_seconds()
                else:
                    hb_age = (now - last_hb).total_seconds()
            except:
                hb_age = float('inf')
        
        # Count consecutive probe failures
        consec_fail = count_consecutive_failures(client_id)
        
        # Determine issues
        heartbeat_bad_offline = hb_age > config.HEARTBEAT_OFFLINE_THRESHOLD
        heartbeat_bad_warn = (hb_age > config.HEARTBEAT_WARNING_THRESHOLD and hb_age <= config.HEARTBEAT_OFFLINE_THRESHOLD)
        probes_offline = consec_fail >= config.PROBE_OFFLINE_CONSECUTIVE
        probes_warn = (consec_fail >= config.PROBE_WARNING_CONSECUTIVE and consec_fail < config.PROBE_OFFLINE_CONSECUTIVE)
        tcp_bad = (tcp_connected == 0)
        
        # Apply priority rules - OFFLINE first
        new_status = current_status
        
        if heartbeat_bad_offline or probes_offline or (tcp_bad and hb_age > config.HEARTBEAT_OFFLINE_THRESHOLD):
            new_status = 'OFFLINE'
        elif heartbeat_bad_warn or probes_warn or tcp_bad:
            if current_status == 'OFFLINE':
                # Check if can recover
                if hb_age <= config.HEARTBEAT_WARNING_THRESHOLD and consec_fail < config.PROBE_WARNING_CONSECUTIVE and tcp_connected == 1:
                    new_status = 'ONLINE'
                else:
                    new_status = 'OFFLINE'
            else:
                new_status = 'WARNING'
        else:
            # All healthy
            if tcp_connected == 1 and hb_age <= config.HEARTBEAT_WARNING_THRESHOLD and consec_fail < config.PROBE_WARNING_CONSECUTIVE:
                new_status = 'ONLINE'
            elif current_status == 'OFFLINE':
                new_status = 'WARNING'
            else:
                new_status = current_status
        
        # Handle status transition
        if new_status != current_status:
            # Create alert
            alert_type = 'STATUS_CHANGE'
            message = f"Client {client['client_name']} ({client['ip_address']}) status changed from {current_status} to {new_status}"
            severity = 'HIGH' if new_status == 'OFFLINE' else ('MEDIUM' if new_status == 'WARNING' else 'LOW')
            
            if heartbeat_bad_offline and new_status == 'OFFLINE':
                alert_type = 'HEARTBEAT_MISS'
                message = f"Client {client['client_name']} offline - no heartbeat for {int(hb_age)}s"
                severity = 'HIGH'
            elif probes_offline and new_status == 'OFFLINE':
                alert_type = 'PROBE_FAIL'
                message = f"Client {client['client_name']} offline - {consec_fail} consecutive probe failures"
                severity = 'HIGH'
            elif heartbeat_bad_warn and new_status == 'WARNING':
                alert_type = 'HEARTBEAT_MISS'
                message = f"Client {client['client_name']} warning - heartbeat delayed ({int(hb_age)}s)"
                severity = 'MEDIUM'
            elif probes_warn and new_status == 'WARNING':
                alert_type = 'PROBE_FAIL'
                message = f"Client {client['client_name']} warning - {consec_fail} consecutive probe failures"
                severity = 'MEDIUM'
            
            execute_query(
                "INSERT INTO alerts (client_id, alert_type, message, severity, status_before, status_after, acknowledged) VALUES (?, ?, ?, ?, ?, ?, 0)",
                (client_id, alert_type, message, severity, current_status, new_status)
            )
            
            # Log events
            execute_query(
                "INSERT INTO event_history (client_id, event_type, details) VALUES (?, 'STATUS_CHANGE', ?)",
                (client_id, f"Status: {current_status} -> {new_status}")
            )
            execute_query(
                "INSERT INTO event_history (client_id, event_type, details) VALUES (?, 'ALERT', ?)",
                (client_id, message)
            )
            
            # Update status
            execute_query(
                "UPDATE clients SET status = ?, updated_at = datetime('now','localtime') WHERE id = ?",
                (new_status, client_id)
            )
            print(f"[MONITOR] {client['client_name']}: {current_status} -> {new_status} | HB:{int(hb_age)}s TCP:{tcp_connected} Fail:{consec_fail}")
