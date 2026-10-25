import socket
import json
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001
HEARTBEAT_INTERVAL = 5

def main():
    client_name = 'lab-pc-01'
    ip_address = '192.168.1.100'
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'[UDP] Sending heartbeats to {SERVER_HOST}:{SERVER_PORT}')
    
    while True:
        try:
            heartbeat = {
                'type': 'HEARTBEAT',
                'client_name': client_name,
                'ip_address': ip_address,
                'ts': time.time()
            }
            s.sendto(json.dumps(heartbeat).encode('utf-8'), (SERVER_HOST, SERVER_PORT))
            print(f'[UDP] Heartbeat sent at {time.strftime("%H:%M:%S")}')
            time.sleep(HEARTBEAT_INTERVAL)
        except Exception as e:
            print(f'[UDP] Error: {e}')
            time.sleep(HEARTBEAT_INTERVAL)

if __name__ == '__main__':
    main()
