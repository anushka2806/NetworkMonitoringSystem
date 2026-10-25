# 02 - Status Rules and Thresholds

## Statuses (Exactly Three)
- ONLINE
- WARNING  
- OFFLINE

## Thresholds (Defaults)
| Parameter | Value | Purpose |
|---|---|---|
| HEARTBEAT_INTERVAL | 5s | Client sends UDP heartbeat every 5s |
| HEARTBEAT_WARNING_THRESHOLD | 10s | >10s since last_heartbeat → WARNING consideration |
| HEARTBEAT_OFFLINE_THRESHOLD | 15s | >15s since last_heartbeat → OFFLINE |
| PROBE_INTERVAL | 10s | TCP request/response probe every 10s |
| PROBE_WARNING_CONSECUTIVE | 2 | >=2 consecutive failed probes → WARNING |
| PROBE_OFFLINE_CONSECUTIVE | 4 | >=4 consecutive failed probes → OFFLINE |
| MONITOR_CHECK_INTERVAL | 2-3s | Monitor evaluation frequency |

## Evaluation Rules

### Heartbeat evaluation
1. If `last_heartbeat` is NULL and client just registered with no heartbeats yet:
   - If TCP connected recently and probes OK → may start as WARNING until first heartbeat; after grace period move to OFFLINE per rules.
2. Compute `hb_age = now - last_heartbeat` (seconds). If `hb_age > HEARTBEAT_OFFLINE_THRESHOLD` → heartbeat indicates OFFLINE.
3. If `hb_age > HEARTBEAT_WARNING_THRESHOLD` and `hb_age <= HEARTBEAT_OFFLINE_THRESHOLD` → heartbeat indicates WARNING.

### Probe evaluation
1. Track consecutive failed probes (count of most recent failures in a row). Record each probe in `response_time_probe_history` with success/failure and rtt_ms.
2. If consecutive failures >= PROBE_OFFLINE_CONSECUTIVE → probes indicate OFFLINE.
3. If consecutive failures >= PROBE_WARNING_CONSECUTIVE and < OFFLINE → probes indicate WARNING.

### TCP connection
- `tcp_connected == 1` means persistent TCP connection is active. If it drops to 0 unexpectedly, this is a strong failure signal.

### Status determination (priority)
1. **OFFLINE (highest priority):** If `tcp_connected == 0` AND no recent heartbeat AND probes failing badly → OFFLINE. OR heartbeat age > OFFLINE threshold → OFFLINE. OR probe consecutive failures >= OFFLINE threshold → OFFLINE.
2. **WARNING:** If not OFFLINE but any degradation exists - heartbeat age in WARNING range, or probe failures >= WARNING threshold but < OFFLINE, or TCP connected but heartbeats intermittent.
3. **ONLINE:** Only if TCP connected, heartbeat age <= WARNING threshold (healthy), and recent probes successful (consecutive failures < WARNING threshold), RTT recorded recently.

### Transitions
- On transition ONLINE→WARNING or WARNING→OFFLINE or any→different: create alert in `alerts` with `status_before`, `status_after`, log to `event_history` (STATUS_CHANGE/ALERT).
- Recovery: WARNING→ONLINE or OFFLINE→WARNING/ONLINE also logged.
- Do not spam alerts for same state; only on transition.
