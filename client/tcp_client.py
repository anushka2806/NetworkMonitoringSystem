import socket
import json
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="TCP client for Network Monitoring System")
    parser.add_argument('--server', default='127.0.0.1', help="Server IP (default: 127.0.0.1)")
    parser.add_argument('--port', type=int, default=5000, help="Server TCP port (default: 5000)")
    parser.add_argument('--name', default=socket.gethostname(), help="Client name (default: this PC's hostname)")
    parser.add_argument('--ip', default=None, help="IP to report (default: auto-detect)")
    args = parser.parse_args()

    # Auto-detect this PC's LAN IP if not provided
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
    print(f"[TCP] Client '{client_name}' ({ip_address}) -> {args.server}:{args.port}")

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((args.server, args.port))
            # Register
            reg = {'type': 'REGISTER', 'client_name': client_name, 'ip_address': ip_address}
            s.send(json.dumps(reg).encode('utf-8'))
            resp = s.recv(1024)
            print(f'[TCP] Registration response: {resp.decode()}')
            # Listen for probes
            while True:
                try:
                    data = s.recv(1024)
                    if not data:
                        break
                    msg = json.loads(data.decode('utf-8'))
                    if msg.get('type') == 'PROBE':
                        ts = msg.get('ts')
                        probe_resp = {'type': 'PROBE_RESP', 'ts': ts}
                        s.send(json.dumps(probe_resp).encode('utf-8'))
                        print(f'[TCP] Responded to probe with ts={ts}')
                except socket.timeout:
                    continue
                except:
                    break
            s.close()
        except Exception as e:
            print(f'[TCP] Error: {e}, reconnecting in 5s...')
            time.sleep(5)

if __name__ == '__main__':
    main()
