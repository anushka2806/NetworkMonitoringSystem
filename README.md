Copy this into a file named **`README.md`** in the project root:

```md
# Network Monitoring and Fault Detection System

A Computer Networks mini-project that monitors computers on a network. Clients register with a central server using TCP, send regular UDP heartbeats, and appear on a web dashboard as `ONLINE`, `WARNING`, or `OFFLINE`.

## Features

- TCP-based client registration
- TCP probes for measuring RTT (Round Trip Time)
- UDP heartbeats sent every 5 seconds
- Automatic `ONLINE`, `WARNING`, and `OFFLINE` detection
- Fault alerts when a client stops sending heartbeats
- SQLite database for clients, events, alerts, and probe history
- FastAPI REST API
- React + TypeScript dashboard with charts and client status information
- Support for multiple client PCs on the same network

## Architecture

```text
Client PCs
  ├── TCP registration and probe responses ──► TCP Server (Port 5000)
  └── UDP heartbeats ───────────────────────► UDP Server (Port 5001)
                                                  │
                                           Monitoring Service
                                                  │
                                              SQLite Database
                                                  │
                                         FastAPI API (Port 8001)
                                                  │
                                      React Dashboard (Port 5173)
```

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Networking | Python TCP and UDP sockets |
| Database | SQLite |
| Frontend | React, TypeScript, Vite |
| Charts | Chart.js, react-chartjs-2 |

## Project Structure

```text
NetworkMonitoringSystem/
│
├── backend/
│   ├── app/
│   │   ├── db/             # SQLite schema and database session
│   │   ├── routers/        # FastAPI API routes
│   │   ├── services/       # TCP server, UDP server, monitor service
│   │   ├── config.py       # Port and monitoring configuration
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt
│   └── run.py
│
├── client/
│   ├── tcp_client.py       # Client registration and TCP probe response
│   └── udp_heartbeat.py    # UDP heartbeat sender
│
├── frontend/
│   └── src/                # React dashboard
│
├── documentation/          # Project documentation
└── implementation_plan/    # Implementation plan
```

## Prerequisites

- Python 3.10 or newer
- Node.js and npm
- Windows PowerShell

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/anushka2806/NetworkMonitoringSystem.git
cd NetworkMonitoringSystem
```

### 2. Set up the Python backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### 3. Install frontend packages

```powershell
cd frontend
npm install
cd ..
```

## Run the Project Locally

Open separate PowerShell terminals for the backend, frontend, TCP client, and UDP client.

### Terminal 1 — Start the backend

```powershell
cd C:\Users\ASUS\NetworkMonitoringSystem
.\.venv\Scripts\Activate.ps1
python -m backend.run
```

Successful output should include:

```text
[TCP] Server listening on 0.0.0.0:5000
[UDP] Server listening on 0.0.0.0:5001
INFO: Uvicorn running on http://127.0.0.1:8001
```

### Terminal 2 — Start the frontend dashboard

```powershell
cd C:\Users\ASUS\NetworkMonitoringSystem\frontend
npm run dev
```

Open the Vite URL shown in the terminal, usually:

```text
http://localhost:5173
```

### Terminal 3 — Start the TCP client

```powershell
cd C:\Users\ASUS\NetworkMonitoringSystem
.\.venv\Scripts\Activate.ps1
python client\tcp_client.py --name my-pc
```

Expected output:

```text
[TCP] Registration response: {"status": "OK", "message": "Registered"}
```

### Terminal 4 — Start the UDP heartbeat client

```powershell
cd C:\Users\ASUS\NetworkMonitoringSystem
.\.venv\Scripts\Activate.ps1
python client\udp_heartbeat.py --name my-pc
```

The client sends a heartbeat every 5 seconds:

```text
[UDP] Heartbeat sent at 15:30:05
[UDP] Heartbeat sent at 15:30:10
```

Within a few seconds, the dashboard should show the client as `ONLINE`.

## Adding Multiple Client PCs

The backend PC acts as the monitoring server. Other PCs act as clients.

### 1. Find the server PC IP address

On the PC running the backend:

```powershell
ipconfig
```

Find the active adapter's IPv4 address. Example:

```text
10.251.209.159
```

Both PCs must be connected to the same Wi-Fi, LAN, or hotspot.

### 2. Open firewall ports on the server PC

Run PowerShell as **Administrator** on the server PC:

```powershell
New-NetFirewallRule -DisplayName "NetMonitor TCP 5000" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow -Profile Any

New-NetFirewallRule -DisplayName "NetMonitor UDP 5001" -Direction Inbound -Protocol UDP -LocalPort 5001 -Action Allow -Profile Any
```

### 3. Copy client files to the partner PC

Copy these files to the partner's computer:

```text
client/tcp_client.py
client/udp_heartbeat.py
```

The partner PC needs Python installed. No extra Python packages are needed.

### 4. Run TCP registration on the partner PC

Replace the IP address with the server PC's current IP:

```powershell
python tcp_client.py --server 10.251.209.159 --name partner-pc
```

### 5. Run UDP heartbeat on the partner PC

Open another terminal:

```powershell
python udp_heartbeat.py --server 10.251.209.159 --name partner-pc
```

Important: the `--name` value must be the same in both commands.

The dashboard should show both `my-pc` and `partner-pc`.

## Client Command Arguments

| Argument | Description |
|---|---|
| `--server` | Server IP address. Default: `127.0.0.1` |
| `--port` | Server port number |
| `--name` | Unique name for the client PC |
| `--ip` | Optional IP address to report |
| `--interval` | UDP heartbeat interval in seconds |

Example:

```powershell
python tcp_client.py --server 10.251.209.159 --name lab-pc-01

python udp_heartbeat.py --server 10.251.209.159 --name lab-pc-01 --interval 5
```

## Status Rules

| Condition | Status |
|---|---|
| Recent heartbeat and successful TCP probes | `ONLINE` |
| No heartbeat for more than 10 seconds | `WARNING` |
| No heartbeat for more than 15 seconds | `OFFLINE` |
| Four consecutive TCP probe failures | `OFFLINE` |

## RTT Explanation

RTT means **Round Trip Time**.

The server sends a TCP probe to a client and waits for the reply. The total time taken for the message to go from the server to the client and back is the RTT.

- Low RTT means a fast connection.
- High RTT can indicate congestion or a slow network.
- Localhost RTT is usually below 1 ms.
- LAN RTT is often between 1 and 10 ms.

## Fault Detection Demo

To demonstrate fault detection:

1. Start the backend, frontend, TCP client, and UDP client.
2. Confirm the client is `ONLINE`.
3. Stop the UDP heartbeat terminal using `Ctrl+C`.
4. After about 10 seconds, the client becomes `WARNING`.
5. After about 15 seconds, it becomes `OFFLINE`.
6. Restart the UDP heartbeat script.
7. The client becomes `ONLINE` again.

## Troubleshooting

### `WinError 10061: No connection could be made`

This means the TCP server is unavailable or the client is pointing to the wrong IP address.

On the server PC, confirm that TCP port 5000 is listening:

```powershell
Get-NetTCPConnection -LocalPort 5000 -State Listen
```

Test locally:

```powershell
Test-NetConnection 127.0.0.1 -Port 5000
```

Expected result:

```text
TcpTestSucceeded : True
```

### Partner can ping the server but cannot connect using TCP

Ensure the backend is running and firewall rules have been added for TCP port 5000 and UDP port 5001.

From the partner PC, test:

```powershell
Test-NetConnection <SERVER-IP> -Port 5000
```

Example:

```powershell
Test-NetConnection 10.251.209.159 -Port 5000
```

### `Errno 10048: address already in use`

Another process is using the FastAPI port.

Check port 8001:

```powershell
Get-NetTCPConnection -LocalPort 8001
```

Stop the process using the port:

```powershell
Stop-Process -Id <PID> -Force
```

Then restart the backend:

```powershell
python -m backend.run
```

### Dashboard shows client as OFFLINE

Make sure all of these remain running:

1. Backend server
2. TCP client
3. UDP heartbeat client

The TCP client must register successfully before the UDP heartbeats are accepted.

## Validation

Backend check:

```powershell
python -m compileall backend\app
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## License

This project is created for educational purposes as a Computer Networks mini-project.
```
