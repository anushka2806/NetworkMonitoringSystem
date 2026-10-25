import socket
import json
from backend.app import config
from backend.app.db.session import fetch_one, execute_query

def start_udp_server():
    """Start UDP server for heartbeats"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((config.UDP_SERVER_HOST, config.UDP_SERVER_PORT))
        print(f"[UDP] Server listening on {config.UDP_SERVER_HOST}:{config.UDP_SERVER_PORT}")
        while True:
            try:
                data, addr = sock.recvfrom(4096)
                msg = json.loads(data.decode('utf-8'))
                if msg.get('type') == 'HEARTBEAT':
                    client_name = msg.get('client_name')
                    if not client_name:
                        continue
                    client = fetch_one("SELECT * FROM clients WHERE client_name = ?", (client_name,))
                    if client:
                        execute_query("UPDATE clients SET last_heartbeat=datetime('now','localtime'), updated_at=datetime('now','localtime') WHERE id=?", (client['id'],))
                        execute_query("INSERT INTO event_history (client_id, event_type, details) VALUES (?, 'HEARTBEAT', ?)", (client['id'], f"UDP heartbeat received from {addr[0]}"))
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"[UDP] Error: {e}")
                continue
    except Exception as e:
        print(f"[UDP] Server error: {e}")
