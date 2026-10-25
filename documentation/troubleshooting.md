# Troubleshooting Guide

## Overview

Common issues encountered during setup and testing of the Network Monitoring and Fault Detection System, along with solutions.

## Backend Issues

### 1. Port Already in Use
**Error:** `[Errno 98] Address already in use` (Linux) or `[WinError 10048] Only one usage of each socket address` (Windows)

**Cause:** Another process is using TCP/UDP port

**Solutions:**
- **Windows:** `netstat -ano | findstr :5000` to find PID, then `taskkill /PID <pid> /F`
- **Linux/Mac:** `lsof -i :5000` or `netstat -tulnp | grep 5000`
- Change port in `backend/app/config.py`
- Use `SO_REUSEADDR` in socket code (already recommended)

### 2. SQLite Database Locked
**Error:** `sqlite3.OperationalError: database is locked`

**Cause:** Multiple threads/processes accessing SQLite simultaneously without proper handling

**Solutions:**
- Use a single connection or connection pooling carefully
- Use `check_same_thread=False` if needed in some contexts
- Ensure only one writer at a time
- Close connections properly
- For mini-project, threading with proper locks or using same connection is fine

### 3. Module Import Errors
**Error:** `ModuleNotFoundError: No module named 'app'` or similar

**Cause:** Running from wrong directory or PYTHONPATH issues

**Solutions:**
- Run from `backend/` directory: `python run.py`
- Or set PYTHONPATH: `set PYTHONPATH=%PYTHONPATH%;.` (Windows) / `export PYTHONPATH=.` (Linux)
- Ensure `__init__.py` files exist in all packages
- Use relative imports correctly

### 4. FastAPI/Uvicorn Not Starting
**Error:** `ModuleNotFoundError: No module named 'fastapi'` or `uvicorn`

**Cause:** Dependencies not installed

**Solutions:**
- Install requirements: `pip install -r backend/requirements.txt`
- Create venv: `python -m venv venv`, activate it, install
- Check Python version (3.8+)

### 5. Background Tasks Not Running
**Issue:** TCP/UDP servers or monitor not starting with FastAPI

**Cause:** Not started in `@app.on_event("startup")` or main

**Solutions:**
- Start servers/monitor in FastAPI startup event
- Use `asyncio.create_task()` for async functions
- Use threading for blocking socket operations
- Check logs for errors

## Socket Issues

### 6. TCP Connection Refused
**Error:** `ConnectionRefusedError: [Errno 111] Connection refused`

**Cause:** TCP server not running or wrong port/IP

**Solutions:**
- Ensure TCP server is running before starting client
- Check `config.py` for correct TCP_SERVER_HOST/PORT
- Use `127.0.0.1` for localhost testing
- Check firewall settings

### 7. UDP Packets Not Received
**Issue:** Heartbeats sent but last_seen not updated

**Cause:** Wrong port, firewall blocking, or wrong IP

**Solutions:**
- Verify UDP_SERVER_PORT matches in client and server
- Use `0.0.0.0` on server to listen on all interfaces
- Check Windows Firewall/antivirus blocking UDP
- Test with localhost (`127.0.0.1`)
- Add debug prints in UDP server to see if packets arrive

### 8. Client Can't Reach Server on Different Network
**Issue:** Works on localhost but not across machines

**Cause:** Binding to `127.0.0.1` instead of `0.0.0.0`, or firewall

**Solutions:**
- Bind server to `0.0.0.0`
- Use server's actual IP address in client
- Open ports in firewall
- Ensure both machines on same network

## Frontend Issues

### 9. CORS Errors
**Error:** `Access to fetch at ... from origin ... has been blocked by CORS policy`

**Cause:** FastAPI CORS not configured or wrong origins

**Solutions:**
- Add CORSMiddleware in `main.py`
- Include frontend URL in `allow_origins` (e.g., `http://localhost:5173`, `http://localhost:3000`)
- Use `allow_methods=["*"]` and `allow_headers=["*"]` for dev
- Restart backend after changes

### 10. API Fetch Fails
**Error:** Network error or `Failed to fetch`

**Cause:** Backend not running, wrong URL, or API down

**Solutions:**
- Check backend is running at correct URL
- Verify `API_BASE` in `src/services/api.ts`
- Test endpoint in browser: `http://localhost:8000/clients`
- Check browser console for details
- Ensure no proxy issues

### 11. Chart.js Not Rendering
**Issue:** Charts appear blank or errors

**Cause:** Missing imports/registration or wrong data format

**Solutions:**
- Register Chart.js elements: ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend
- Use proper data structure for Pie/Bar charts
- Check console for errors
- Ensure Chart.js and react-chartjs-2 installed (conceptually)
- Use correct chart type

### 12. TypeScript Errors
**Error:** Type mismatches between API and types

**Cause:** Backend response doesn't match TypeScript interfaces

**Solutions:**
- Compare API response with `src/types/index.ts`
- Use optional chaining or adjust interfaces
- Add type assertions carefully (minimal)
- Check actual JSON from API

## Fault Detection Issues

### 13. Client Not Going Offline
**Issue:** Heartbeats stopped but status remains ONLINE

**Cause:** Monitor not running, timeout too long, or last_seen not updated

**Solutions:**
- Ensure monitor service is running in background
- Check `HEARTBEAT_TIMEOUT` value (try smaller for testing, e.g., 15s)
- Verify UDP server actually updates last_seen
- Check monitor logs/prints
- Inspect DB: look at last_seen timestamp

### 14. False Offline Alerts
**Issue:** Client goes offline despite sending heartbeats

**Cause:** Clock differences, timeout too small, or network delays

**Solutions:**
- Increase timeout to 2-3x heartbeat interval
- Use same time source (system clock)
- Check if client clock skewed
- Debug monitor loop timing

### 15. Alerts Not Generated
**Issue:** Status changes to OFFLINE but no alert created

**Cause:** Monitor logic bug or DB error

**Solutions:]
- Check monitor service code logic
- Inspect alerts table directly
- Look for errors in monitor thread/async task
- Ensure alert creation happens before/when status changes

## General Tips
- **Debugging:** Use print statements liberally in sockets/monitor to trace flow
- **Testing:** Start with localhost, use one client first, then scale
- **Logs:** Check events table frequently for system behavior
- **Clean Slate:** Delete `monitor.db` to reset for fresh testing
- **Firewall:** Temporarily disable firewall for testing if issues persist (only in safe environment)
- **Terminal Clarity:** Use different terminal colors/titles for server, client, frontend

## Quick Checklist for Viva Demo
- [ ] Backend running on all ports
- [ ] TCP registration works
- [ ] UDP heartbeats working
- [ ] Fault detection demonstrated (stop heartbeat)
- [ ] Alert generated
- [ ] Dashboard shows live status
- [ ] Charts visible
- [ ] Can explain TCP vs UDP usage
- [ ] Can explain timeout/fault detection
