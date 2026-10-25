# Viva Questions & Answers

## Basic Questions

### Q1. What is the title of your project?
**A:** Network Monitoring and Fault Detection System.

### Q2. What is the objective of your project?
**A:** To register clients, monitor their connectivity using TCP and UDP, measure response times, detect online/offline status, generate fault alerts, log events, and display network status on a web dashboard.

### Q3. What technologies have you used in this project?
**A:** Python and FastAPI for backend, TCP and UDP socket programming for communication, SQLite for database, React.js and TypeScript for frontend, HTML, CSS, and Chart.js for the dashboard.

## Computer Networks Related Questions

### Q4. Why have you used TCP for client registration?
**A:** TCP is connection-oriented and reliable. Registration data must reach the server without loss. Also, TCP demonstrates the 3-way handshake (SYN, SYN-ACK, ACK) which is a key concept in Computer Networks.

### Q5. Why have you used UDP for heartbeats?
**A:** UDP is connectionless and has less overhead. Heartbeats are small periodic messages to check if the client is alive. We don't need guaranteed delivery of every heartbeat - if heartbeats stop coming for a timeout period, we can detect the client as offline. This is efficient and lightweight.

### Q6. What is the difference between TCP and UDP?
**A:** 
- **TCP:** Connection-oriented, reliable, guarantees delivery and order, slower due to overhead (3-way handshake, acknowledgments)
- **UDP:** Connectionless, unreliable, no guarantee of delivery/order, faster with less overhead

### Q7. What is a socket?
**A:** A socket is an endpoint for communication between two machines over a network. It is identified by a combination of IP address and port number. In Python, we use the `socket` module to create TCP (SOCK_STREAM) and UDP (SOCK_DGRAM) sockets.

### Q8. Explain the TCP 3-way handshake.
**A:** TCP establishes connection via:
1. **SYN:** Client sends SYN to server to initiate connection
2. **SYN-ACK:** Server acknowledges and sends SYN
3. **ACK:** Client acknowledges server's SYN
After this, connection is established and data transfer begins.

### Q9. What is a heartbeat in network monitoring?
**A:** A heartbeat is a periodic signal sent by a client to the monitoring server to indicate that it is alive and operational. If the server stops receiving heartbeats within a specified timeout, it assumes the client is down/unreachable.

### Q10. What is RTT and how do you measure it?
**A:** RTT (Round Trip Time) is the time taken for a packet to travel from source to destination and back to the source. In our project, we measure it during TCP connection/registration or track response times and store in `clients.rtt_ms`.

### Q11. How do you detect if a client is offline?
**A:** We track `last_seen` timestamp updated on every UDP heartbeat. The monitor service periodically checks: if (current_time - last_seen) > HEARTBEAT_TIMEOUT and status is ONLINE, we mark it as OFFLINE, generate a fault alert, and log a status change event.

### Q12. What is fault detection?
**A:** Fault detection is the process of identifying failures in the network/system. In our project, when a client stops sending heartbeats beyond the timeout threshold, we detect it as a fault and generate an alert.

## Database & Backend Questions

### Q13. Why did you use SQLite?
**A:** SQLite is lightweight, file-based, serverless, and easy to use. It's perfect for a college mini-project - no separate database server installation needed. It supports standard SQL and is sufficient for storing clients, alerts, and events.

### Q14. What tables are there in your database?
**A:** We have four tables:
- **clients:** Stores client info, status, last_seen, rtt_ms
- **probes:** Monitoring probe configurations (extensible)
- **alerts:** Fault alerts generated on client going offline
- **events:** System event logs (registration, heartbeat, status change)

### Q15. What is FastAPI and why did you use it?
**A:** FastAPI is a modern Python web framework for building APIs. It's fast, easy to use, has automatic data validation, and works well with async operations. We use it to expose REST endpoints for the React dashboard to fetch client status, alerts, and events.

### Q16. What is the role of the monitor service?
**A:** The monitor service runs in the background and continuously checks all registered clients. It compares current time with last heartbeat time, detects timeouts, marks clients offline/online, generates alerts on faults, and logs status change events.

## Frontend Questions

### Q17. Why React.js and TypeScript for frontend?
**A:** React.js helps build dynamic, component-based UIs. TypeScript adds type safety, reducing errors. Together they make the dashboard interactive and maintainable. Chart.js is used for visualizing data.

### Q18. What does your dashboard display?
**A:** The dashboard shows:
- Summary cards (Total Clients, Online, Offline, Unacknowledged Alerts)
- Client status table with details (ID, hostname, IP, status, last seen, RTT)
- Alerts panel with fault alerts
- Recent events log
- Charts showing status distribution and RTT values

### Q19. How does the frontend communicate with backend?
**A:** The React frontend uses Fetch API to make HTTP GET/POST requests to FastAPI REST endpoints (e.g., /clients, /alerts, /status). CORS is enabled on the backend to allow cross-origin requests.

## Implementation & Design Questions

### Q20. Explain the complete flow of your system.
**A:** 
1. Client registers via TCP connection to server
2. Server stores client in DB with status ONLINE, logs registration event
3. Client starts sending UDP heartbeats periodically
4. Server updates last_seen timestamp on each heartbeat
5. Monitor service checks heartbeats - if no heartbeat within timeout, marks client OFFLINE and generates alert
6. FastAPI exposes data via REST API
7. React dashboard fetches and displays this data with charts

### Q21. Can a client be TCP-connected but shown as offline?
**A:** Yes, in our design. TCP connection might be established for registration, but if the client stops sending UDP heartbeats, the monitor will mark it as OFFLINE based on heartbeat timeout. This demonstrates that both protocols serve different purposes.

### Q22. What happens when a client comes back online after being offline?
**A:** When heartbeats resume, the UDP server updates last_seen. On next monitor check, if it was OFFLINE and now has recent heartbeat, the monitor marks it ONLINE again and logs a STATUS_CHANGE event.

### Q23. Why run TCP and UDP servers on different ports?
**A:** TCP and UDP are different transport protocols - they are independent. Using different ports avoids conflicts and clearly demonstrates both protocols. Also, it's easier to test them separately.

### Q24. What are the advantages of your system?
**A:** 
- Demonstrates both TCP and UDP socket programming
- Real-time fault detection using heartbeats
- Simple and easy to understand
- Web-based visualization
- Lightweight using SQLite
- Good for learning network monitoring concepts

### Q25. What improvements can be made?
**A:** Add authentication, email/SMS alerts, graphical network topology, SNMP support, threshold-based alerts, historical data analysis, or use of ICMP ping. But for a mini-project, our current implementation covers all required features.

## Quick Tips for Viva
- Emphasize **TCP vs UDP distinction** - very important
- Be able to draw/explain the architecture diagram mentally
- Know the heartbeat timeout logic clearly
- Explain why connectionless UDP is suitable for heartbeats
- Demonstrate the flow: register → heartbeat → fault → alert → dashboard
- Be ready to show the code structure briefly
