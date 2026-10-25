# Network Monitoring and Fault Detection System - Index

## Project Overview

**Project Title:** Network Monitoring and Fault Detection System  
**Type:** Computer Networks Mini-Project  
**Target Audience:** College Students (for learning and viva demonstration)  
**Objective:** To design and implement a network monitoring system that can register clients, monitor their connectivity status using TCP and UDP, detect faults, generate alerts, and display real-time network status through a web dashboard.

## Problem Statement

The system must register clients, monitor TCP connections and UDP heartbeats, measure response times (RTT), detect online/offline status, generate fault alerts, log events, and display network status on a dashboard.

## Tech Stack

| Component | Technology | Purpose |
| :-- | :-- | :-- |
| **Backend Framework** | [Python](https://www.python.org/) + [FastAPI](https://fastapi.dev/) | REST API endpoints to serve client data, alerts, events and status |
| **TCP Socket Programming** | Python `socket` module (TCP) | Client registration, connection tracking and TCP-based monitoring |
| **UDP Socket Programming** | Python `socket` module (UDP) | Lightweight heartbeat monitoring for real-time connectivity checks |
| **Database** | [SQLite](https://www.sqlite.org/) | Persistent storage for clients, probes, alerts and events |
| **Frontend Framework** | [React.js](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) | Interactive web dashboard for visualization |
| **Markup & Styling** | [HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS) | Structure and styling of the dashboard |
| **Data Visualization** | [Chart.js](https://www.chartjs.org/) | Graphical representation of uptime, RTT and alerts |

## Tools Used

- **Code Editor:** VS Code / any Python/Node.js compatible editor
- **Backend Server:** Uvicorn (ASGI server for FastAPI)
- **Package Management:** pip (Python), npm (Node.js)
- **Database Browser:** DB Browser for SQLite (optional, for inspection)
- **Network Testing:** Multiple terminal instances for simulating clients and servers

## Key Features

1. **Client Registration** - Clients register themselves with the monitoring server via TCP
2. **TCP Connection Monitoring** - Track active TCP connections and measure response times
3. **UDP Heartbeat Monitoring** - Periodic heartbeats sent over UDP for connectivity checks
4. **RTT Measurement** - Calculate Round Trip Time for network performance monitoring
5. **Online/Offline Detection** - Automatic status detection based on heartbeats and TCP connectivity
6. **Fault Detection** - Identify network faults when clients go offline or become unresponsive
7. **Alert Generation** - Generate alerts on fault detection with timestamps
8. **Event Logging** - Log all significant events (registration, status change, alerts)
9. **Real-time Dashboard** - Web-based dashboard displaying client status, alerts, events and statistics
10. **Data Visualization** - Charts showing uptime trends and RTT metrics

## System Architecture Overview

```
┌─────────────┐     TCP/UDP      ┌─────────────────────────────────────────┐
│   Clients    │ ◄──────────────► │         Monitoring Server                │
│ (tcp_client  │                  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  udp_beat)   │                  │  │ TCP Srv  │ │ UDP Srv  │ │ Monitor │ │
└─────────────┘                  │  └──────────┘ └──────────┘ └─────────┘ │
                                 │                │              │         │
                                 │              ┌─▼──────────────▼─┐       │
                                 │              │   SQLite DB       │       │
                                 │              └─────────┬─────────┘       │
                                 │                        │                 │
                                 │                    ┌───▼───┐             │
                                 │                    │FastAPI│             │
                                 │                    └───┬───┘             │
                                 └────────────────────────┼─────────────────┘
                                                          │ REST API
                                                          ▼
                                                    ┌─────────────┐
                                                    │ React + TS   │
                                                    │  Dashboard   │
                                                    │ (Chart.js)   │
                                                    └─────────────┘
```

## Component Interaction Flow

1. **Client Registration:** Client uses TCP to connect to server, sends registration info → Server stores in DB, logs event
2. **Heartbeat:** Client sends periodic UDP heartbeats → Server updates `last_seen` timestamp
3. **Monitoring:** Monitor service checks heartbeats - if no heartbeat within timeout → marks offline, generates alert, logs event
4. **Data Exposure:** FastAPI reads from SQLite and exposes REST endpoints
5. **Visualization:** React dashboard fetches data via API and displays in tables and charts

## Project Structure

See the root `README.md` for detailed folder structure. All source code, documentation and auxiliary scripts are organized systematically.

## Documentation Files

- [`architecture.md`](./architecture.md) - Detailed system architecture
- [`database-schema.md`](./database-schema.md) - SQLite schema design
- [`socket-design.md`](./socket-design.md) - TCP/UDP socket implementation details
- [`api-reference.md`](./api-reference.md) - REST API endpoints
- [`frontend-design.md`](./frontend-design.md) - Frontend design and components
- [`implementation-guide.md`](./implementation-guide.md) - Step-by-step implementation
- [`testing-plan.md`](./testing-plan.md) - Testing strategy and test cases
- [`troubleshooting.md`](./troubleshooting.md) - Common issues and fixes
- [`glossary.md`](./glossary.md) - Computer Networks terminology
- [`viva-questions.md`](./viva-questions.md) - Viva preparation Q&A
- [`agentlog.md`](./agentlog.md) - Agent activity log

## License & Usage

This is an educational mini-project for Computer Networks coursework. 
