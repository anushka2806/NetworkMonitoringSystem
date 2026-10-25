# Socket Design (TCP & UDP)

## Overview

This project demonstrates both major transport layer protocols from Computer Networks:
- **TCP (Transmission Control Protocol)** - Connection-oriented, reliable
- **UDP (User Datagram Protocol)** - Connectionless, unreliable but fast

## Why TCP for Registration?

**Reasons:**
- **Reliability:** Registration data must reach the server. TCP ensures delivery via acknowledgments.
- **Connection Establishment:** Demonstrates 3-way handshake (SYN, SYN-ACK, ACK) - important for viva
- **Ordered Delivery:** Ensures registration payload is received completely and in order
- **Connection Tracking:** Server knows which clients are actively connected via TCP

**Use Case:** Client initiates TCP connection → Server accepts → Exchange registration info → Connection established/tracked.

## Why UDP for Heartbeats?

**Reasons:**
- **Low Overhead:** No connection setup/teardown (no handshake). Less overhead than TCP
- **Lightweight:** Heartbeat packets are small (just client_id + timestamp)
- **Speed:** Faster transmission, ideal for frequent periodic updates
- **Connectionless Nature:** Perfect for "are you alive?" checks - we care about periodic presence, not guaranteed delivery of every packet
- **Real-world Analogy:** Similar to how some monitoring systems use ICMP/pings or UDP beacons

**Key Point:** If UDP heartbeat is missed for longer than timeout, we infer the client is unreachable/offline (could be down, network issue, etc.)

## TCP Server Design

### Configuration
- **Host:** `0.0.0.0` or `127.0.0.1` (localhost for demo)
- **Port:** e.g., `5000` (configurable in `config.py`)

### Flow
```python
# Pseudocode
1. Create socket: socket(AF_INET, SOCK_STREAM)
2. Set socket options: SO_REUSEADDR
3. Bind to (host, port)
4. Listen with backlog
5. Accept connections in loop
6. For each client: handle in thread/async
   - Receive registration data (JSON or delimited)
   - Parse client_id, hostname, ip
   - Update DB: insert/update client, set status=ONLINE, log event
   - Send acknowledgment
7. Track active connections
```

### Registration Payload (Example)
```json
{
  "type": "REGISTER",
  "client_id": "client-01",
  "hostname": "LAB-PC-1",
  "ip_address": "192.168.1.100"
}
```

### RTT Measurement Idea (TCP)
We can measure approximate RTT during registration:
- Record `t1 = time.time()` before sending/after connect
- Or measure response time to ACK
- Store in `clients.rtt_ms`

## UDP Server Design

### Configuration
- **Host:** `0.0.0.0`
- **Port:** e.g., `5001` (different from TCP port)

### Flow
```python
# Pseudocode
1. Create socket: socket(AF_INET, SOCK_DGRAM)
2. Bind to (host, port)
3. Listen for datagrams in loop
4. For each datagram:
   - Decode payload
   - Parse client_id, timestamp
   - Find client in DB
   - Update last_seen = current time
   - If status was OFFLINE, set to ONLINE and log event
   - (Optionally respond with ACK)
```

### Heartbeat Payload (Example)
```json
{
  "type": "HEARTBEAT",
  "client_id": "client-01",
  "timestamp": 1698136245.123
}
```

**Note:** UDP is connectionless, so we just receive packets - no accept() like TCP.

## Heartbeat Timeout & Fault Detection

### Timeout Calculation
- **HEARTBEAT_INTERVAL:** How often client sends heartbeat (e.g., 5 seconds)
- **HEARTBEAT_TIMEOUT:** Max allowed time since last heartbeat (e.g., 15 seconds)
  - Recommended: timeout = 2-3 * interval to account for network delays/loss

### Detection Logic
```python
current_time = datetime.now()
for client in all_clients:
    last_seen = client.last_seen
    delta = (current_time - last_seen).total_seconds()
    if delta > HEARTBEAT_TIMEOUT:
        if client.status == 'ONLINE':
            # Fault detected
            mark_offline(client)
            create_alert(client, "FAULT", f"Client {client.client_id} offline")
            log_event("STATUS_CHANGE", client.client_id, ...)
    else:
        if client.status == 'OFFLINE':
            # Client came back online
            mark_online(client)
            log_event("STATUS_CHANGE", client.client_id, ...)
```

## Socket Addressing

- **AF_INET:** IPv4 addressing
- **SOCK_STREAM:** TCP
- **SOCK_DGRAM:** UDP

## Important Socket Concepts for Viva

| Concept | Explanation |
| :-- | :-- |
| **Socket** | Endpoint of a two-way communication link between two programs on the network |
| **TCP Handshake** | Three-way process (SYN-SYN/ACK-ACK) to establish reliable connection |
| **UDP Datagram** | Self-contained, independent packet sent over connectionless protocol |
| **Binding** | Associating socket with IP address and port |
| **Listening** | TCP server ready to accept connections |
| **Timeout** | Maximum time to wait for expected activity before declaring failure |
| **RTT (Round Trip Time)** | Time for a packet to travel from source to destination and back |
| **Connectionless vs Connection-oriented** | UDP no connection, TCP requires established connection |

## Implementation Notes

- Use `socket.SO_REUSEADDR` to avoid "Address already in use" errors during testing
- Run TCP and UDP servers on different ports
- Handle multiple clients concurrently (threading/asyncio)
- For localhost testing, use `127.0.0.1`
- Keep payloads simple and human-readable (JSON) for easy debugging
- All socket operations in Python's standard library - no extra dependencies

## Testing Scenarios

1. **TCP Registration:** Start server, start tcp_client → connection established, client in DB
2. **UDP Heartbeat:** Start udp_heartbeat → server updates last_seen
3. **Normal Operation:** Status remains ONLINE
4. **Fault Simulation:** Stop udp_heartbeat → after timeout, status becomes OFFLINE, alert generated
5. **Recovery:** Restart heartbeat → status becomes ONLINE again
6 **Mixed Traffic:** Both TCP and UDP working simultaneously
