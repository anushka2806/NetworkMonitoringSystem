import socket
import json
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def main():
    client_name = 'lab-pc-01'
    ip_address = '192.168.1.100'
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_HOST, SERVER_PORT))
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
