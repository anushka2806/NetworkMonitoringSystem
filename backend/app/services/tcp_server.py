import socket
import threading
import json
import time
from datetime import datetime
from backend.app import config
from backend.app.db.session import fetch_one, fetch_all, execute_query

clients_connections = {}  # client_id -> {'socket': sock, 'last_probe': time.time(), 'pending': {}}

def start_tcp_server():
    """Start TCP server for registration and probes"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((config.TCP_SERVER_HOST, config.TCP_SERVER_PORT))
        server_socket.listen(10)
        print(f"[TCP] Server listening on {config.TCP_SERVER_HOST}:{config.TCP_SERVER_PORT}")
        while True:
            try:
                client_sock, addr = server_socket.accept()
                thread = threading.Thread(target=handle_tcp_client, args=(client_sock, addr), daemon=True)
                thread.start()
            except Exception as e:
                print(f"[TCP] Accept error: {e}")
                time.sleep(1)
    except Exception as e:
        print(f"[TCP] Error: {e}")

def handle_tcp_client(client_sock, addr):
    """Handle TCP client connection"""
    client_id = None
    try:
        client_sock.settimeout(30)
        data = client_sock.recv(4096).decode('utf-8')
        msg = json.loads(data)
        if msg.get('type') == 'REGISTER':
            client_name = msg.get('client_name')
            ip_address = msg.get('ip_address', addr[0])
            existing = fetch_one("SELECT * FROM clients WHERE client_name = ?", (client_name,))
            if existing:
                client_id = existing['id']
                execute_query("UPDATE clients SET ip_address=?, tcp_connected=1, updated_at=datetime('now','localtime') WHERE id=?", (ip_address, client_id))
            else:
                execute_query("INSERT INTO clients (client_name, ip_address, tcp_connected, status) VALUES (?, ?, 1, 'WARNING')", (client_name, ip_address))
                client = fetch_one("SELECT id FROM clients WHERE client_name = ?", (client_name,))
                client_id = client['id']
                execute_query("INSERT INTO event_history (client_id, event_type, details) VALUES (?, 'REGISTER', ?)", (client_id, f"Client registered from {ip_address} via TCP"))
            clients_connections[client_id] = {'socket': client_sock, 'last_probe': time.time(), 'pending': {}}
            client_sock.send(json.dumps({"status": "OK", "message": "Registered"}).encode('utf-8'))
            client_sock.settimeout(None)
            # Start probe thread for this client
            probe_thread = threading.Thread(target=probe_client, args=(client_id,), daemon=True)
            probe_thread.start()
            # Keep connection alive and handle responses
            while True:
                try:
                    resp_data = client_sock.recv(1024)
                    if not resp_data:
                        break
                    try:
                        resp_msg = json.loads(resp_data.decode('utf-8'))
                        if resp_msg.get('type') == 'PROBE_RESP':
                            ts = resp_msg.get('ts')
                            if client_id in clients_connections and ts in clients_connections[client_id]['pending']:
                                send_time = clients_connections[client_id]['pending'].pop(ts)
                                rtt_ms = (time.time() - send_time) * 1000
                                execute_query("INSERT INTO response_time_probe_history (client_id, rtt_ms, success, probe_type) VALUES (?, ?, 1, 'TCP')", (client_id, rtt_ms))
                                execute_query("UPDATE clients SET last_probe_at=datetime('now','localtime'), rtt_ms=?, updated_at=datetime('now','localtime') WHERE id=?", (rtt_ms, client_id))
                    except:
                        pass
                except socket.timeout:
                    continue
                except:
                    break
    except Exception as e:
        print(f"[TCP] Client handler error: {e}")
    finally:
        if client_id and client_id in clients_connections:
            try:
                execute_query("UPDATE clients SET tcp_connected=0 WHERE id=?", (client_id,))
            except:
                pass
            del clients_connections[client_id]
        try:
            client_sock.close()
        except:
            pass

def probe_client(client_id):
    """Send periodic probes to client"""
    while client_id in clients_connections:
        try:
            time.sleep(config.PROBE_INTERVAL)
            if client_id not in clients_connections:
                break
            sock = clients_connections[client_id]['socket']
            ts = time.time()
            clients_connections[client_id]['pending'][ts] = ts
            probe_msg = json.dumps({"type": "PROBE", "ts": ts}).encode('utf-8')
            try:
                sock.send(probe_msg)
                # Wait a bit for response
                time.sleep(3)
                # If still pending after timeout, record as failed
                if client_id in clients_connections and ts in clients_connections[client_id]['pending']:
                    clients_connections[client_id]['pending'].pop(ts)
                    execute_query("INSERT INTO response_time_probe_history (client_id, rtt_ms, success, probe_type) VALUES (?, 0, 0, 'TCP')", (client_id,))
                    execute_query("UPDATE clients SET last_probe_at=datetime('now','localtime'), updated_at=datetime('now','localtime') WHERE id=?", (client_id,))
            except:
                break
        except Exception as e:
            break
