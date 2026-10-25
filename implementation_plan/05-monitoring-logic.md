# 05 - Monitoring Logic

## Goals
- Background monitor evaluating all clients against thresholds
- Apply ONLINE/WARNING/OFFLINE rules
- Generate alerts on status transitions
- Log to event_history
- Update client status

## Evaluation Flow (every MONITOR_CHECK_INTERVAL)
For each client in `clients`:
1. **Get timestamps**: `now`, `last_heartbeat`, `last_probe_at`, `tcp_connected`
2. **Compute ages**: `hb_age` (seconds since last_heartbeat; if NULL treat as large), `probe_age`
3. **Get probe history**: count consecutive failures from most recent probes
4. **Determine candidate issues**:
   - heartbeat_bad_offline = (hb_age > HEARTBEAT_OFFLINE_THRESHOLD)
   - heartbeat_bad_warn = (hb_age > HEARTBEAT_WARNING_THRESHOLD and not heartbeat_bad_offline)
   - probes_offline = (consec_fail >= PROBE_OFFLINE_CONSECUTIVE)
   - probes_warn = (consec_fail >= PROBE_WARNING_CONSECUTIVE and not probes_offline)
   - tcp_bad = (tcp_connected == 0)
5. **Apply priority (OFFLINE first)**:
   - If heartbeat_bad_offline OR probes_offline OR (tcp_bad AND hb_age > OFFLINE threshold): new_status = 'OFFLINE'
   - Elif heartbeat_bad_warn OR probes_warn OR (tcp_bad): new_status = 'WARNING' (if not offline)
   - Else: new_status = 'ONLINE' (healthy)
6. **Transition handling**:
   - If new_status != current_status:
     * Create alert in `alerts` (alert_type based on cause, message, status_before/current, status_after/new)
     * Insert event_history STATUS_CHANGE with details
     * Update `clients.status = new_status`, `clients.updated_at = now`
7. **No change**: just update timestamps if needed

## Alert Types
- HEARTBEAT_MISS (heartbeat timeout)
- PROBE_FAIL (consecutive probe failures)
- TIMEOUT (combined)
- STATUS_CHANGE (general)

## Concurrency
- Run as background thread (daemon) started from FastAPI startup
- Access DB safely (use connections per operation or locks)
- Must not block HTTP

## Files
- `backend/app/services/monitor.py`
