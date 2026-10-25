# Testing Plan

## Overview

This plan covers manual testing of all components - TCP/UDP sockets, fault detection, API, and dashboard.

## Test Environment Setup
- Multiple terminal windows
- Backend server running
- 1-2 client agents running
- Frontend running in browser
- DB Browser for SQLite (optional) to inspect tables

## Test Cases

### 1. Database Initialization
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| DB-01 | Run backend first time | `monitor.db` created with all 4 tables | Pass/Fail |
| DB-02 | Check schema | Tables: clients, probes, alerts, events exist | Pass/Fail |

### 2. TCP Registration
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| TCP-01 | Start TCP server, run tcp_client.py | Connection established successfully | Pass/Fail |
| TCP-02 | Register client-01 | Client appears in `clients` table with status ONLINE | Pass/Fail |
| TCP-03 | Check events log | Event with type REGISTER logged for client-01 | Pass/Fail |
| TCP-04 | Register same client again | No duplicate created, existing record updated | Pass/Fail |
| TCP-05 | Multiple clients register | All appear in database | Pass/Fail |

### 3. UDP Heartbeat Monitoring
| Test ID | Description | Expected Result | Status |
| :-- | :tag]] | :-- | :-- |
| UDP-01 | Start udp_heartbeat.py after registration | Heartbeats sent every interval | Pass/Fail |
| UDP-02 | Check last_seen update | `last_seen` timestamp updates with each heartbeat | Pass/Fail |
| UDP-02b | Heartbeat received event | Event type HEARTBEAT logged (optional) | Pass/Fail |
| UDP-03 | Status remains ONLINE | Client status stays ONLINE while heartbeats continue | Pass/Fail |

### 4. Fault Detection & Alerts
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| FD-01 | Stop udp_heartbeat.py (keep TCP client maybe stopped) | Monitor detects no heartbeat | Pass/Fail |
| FD-02 | Wait for timeout period (> HEARTBEAT_TIMEOUT) | Client status changes to OFFLINE | Pass/Fail |
| FD-03 | Alert generation | Alert created in `alerts` table with type FAULT | Pass/Fail |
| FD-04 | Event logging | STATUS_CHANGE and ALERT events logged | Pass/Fail |
| FD-05 | Severity assigned | Alert has appropriate severity (e.g., HIGH) | Pass/Fail |
| FD-06 | Multiple clients - only missing ones affected | Other clients remain ONLINE if heartbeating | Pass/Fail |

### 5. Recovery (Online After Offline)
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| REC-01 | Restart udp_heartbeat.py for offline client | Heartbeats resume | Pass/Fail |
| REC-02 | Monitor detects activity | Status changes from OFFLINE to ONLINE | Pass/Fail |
| REC-03 | Event logged | STATUS_CHANGE event logged for recovery | Pass/Fail |
| REC-04 | last_seen updated | last_seen becomes current timestamp | Pass/Fail |

### 6. RTT Measurement
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| RTT-01 | After registration/connection | RTT value calculated and stored in clients.rtt_ms | Pass/Fail |
| RTT-02 | RTT visible in DB | Non-zero value for active clients | Pass/Fail |
| RTT-03 | RTT displayed on dashboard | RTT column shows values in ms | Pass/Fail |

### 7. FastAPI REST Endpoints
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| API-01 | GET /clients | Returns list of all clients with correct fields | Pass/Fail |
| API-02 | GET /clients/{client_id} | Returns specific client or 404 if not exists | Pass/Fail |
| API-03 | GET /status | Returns summary with counts correct | Pass/Fail |
| API-04 | GET /alerts | Returns alerts, newest first | Pass/Fail |
| API-05 | POST /alerts/{id}/ack | Acknowledges alert, acknowledged becomes 1 | Pass/Fail |
| API-06 | GET /events?limit=10 | Returns limited events, newest first | Pass/Fail |
| API-07 | GET /health | Returns healthy status | Pass/Fail |
| API-08 | CORS enabled | Frontend can fetch without CORS errors | Pass/Fail |

### 8. Frontend Dashboard
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| UI-01 | Dashboard loads | All components render without errors | Pass/Fail |
| UI-02 | Status cards show correct counts | Total/Online/Offline/Alerts match DB/API | Pass/Fail |
| UI-03 | Client table displays all clients | All registered clients shown with status badges | Pass/Fail |
| UI-04 | Status badges color-coded | ONLINE = green, OFFLINE = red | Pass/Fail |
| UI-05 | Alerts panel shows alerts | Fault alerts displayed with severity | Pass/Fail |
| UI-06 | Acknowledge button works | Clicking ack updates alert status | Pass/Fail |
| UI-07 | Event log shows recent events | Latest events displayed in order | Pass/Fail |
| UI-08 | Chart.js renders pie chart | Status distribution chart visible | Pass/Fail |
| UI-09 | Chart.js renders bar chart | RTT chart visible for clients with RTT | Pass/Fail |
| UI-10] | Auto-refresh (if implemented) | Data updates without manual page refresh | Pass/Fail |

## Integration Test Scenario

**Scenario: Full System Demo**
1. Start backend (all servers + monitor + API)
2. Start tcp_client.py for client-01
3. Start udp_heartbeat.py for client-01
4. Open frontend dashboard - client-01 should be ONLINE
5. Stop udp_heartbeat.py
6. Wait ~15-20 seconds (timeout period)
7. Dashboard should show client-01 as OFFLINE, alert generated
8. Restart udp_heartbeat.py
9. Wait a few seconds - client-01 should become ONLINE again
10. Verify all events logged

## Performance/Edge Cases
| Test ID | Description | Expected Result | Status |
| :-- | :-- | :-- | :-- |
| EDGE-01 | Client sends heartbeat before TCP registration | UDP server handles gracefully (may log or ignore) | Pass/Fail |
| EDGE-02 | Server restart | Clients remain in DB; monitor resumes checking | Pass/Fail |
| EDGE-03 | Multiple heartbeats in quick succession | Last seen updated correctly, no errors | Pass/Fail |
| EDGE-04 | Port already in use | Clear error message or handle with SO_REUSEADDR | Pass/Fail |

## Testing Tools
- **Browser DevTools:** Check network requests, console errors
- **DB Browser for SQLite:** Inspect tables directly
- **curl/Postman:** Test API endpoints individually
- **Multiple terminals:** Simulate clients/servers
 

## Notes
- Adjust timeout values for faster testing (ebl connections/bypassing full timeout)
- Clean DB between tests if needed (delete monitor.db)
- For viva, demonstrate all three aspects: TCP registration, UDP heartbeats, Fault detection
