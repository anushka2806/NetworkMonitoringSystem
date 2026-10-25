import socket
import json
import time
import argparse

HEARTBEAT_INTERVAL = 5

def main():
    parser = argparse.ArgumentParser(description="UDP heartbeat client for Network Monitoring System")
    parser.add_argument('--server', default='127.0.0.1', help="Server IP (default: 127.0.0.1)")
    parser.add_argument('--port', type=int, default=5001, help="Server UDP port (default: 5001)")
    parser.add_argument('--name', default=socket.gethostname(), help="Client name (must match TCP client --name)")
    parser.add_argument('--ip', default=None, help="IP to report (default: auto-detect)")
    parser.add_argument('--interval', type=int, default=HEARTBEAT_INTERVAL, help="Heartbeat interval in seconds")
    args = parser.parse_args()

    # Auto-detect LAN IP
    if args.ip:
        ip_address = args.ip
    else:
        try:
            s_tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_tmp.connect(("8.8.8.8", 80))
            ip_address = s_tmp.getsockname()[0]
            s_tmp.close()
        except Exception:
            ip_address = '127.0.0.1'

    client_name = args.name
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[UDP] Client '{client_name}' ({ip_address}) -> {args.server}:{args.port} every {args.interval}s")

    while True:
        try:
            heartbeat = {
                'type': 'HEARTBEAT',
                'client_name': client_name,
                'ip_address': ip_address,
                'ts': time.time()
            }
            s.sendto(json.dumps(heartbeat).encode('utf-8'), (args.server, args.port))
            print(f'[UDP] Heartbeat sent at {time.strftime("%H:%M:%S")}')
            time.sleep(args.interval)
        except Exception as e:
            print(f'[UDP] Error: {e}')
            time.sleep(args.interval)

if __name__ == '__main__':
    main()
