# Cell Collective Simulation Architecture

## Summary

Cell Collective uses **Socket.IO (WebSocket)** for real-time simulation communication. This document explains what we discovered and how to implement it.

---

## What We Captured

From `teach.cellcollective.orgsimulation.har`, we discovered:

### 1. Socket.IO Connection Flow

```
1. HTTP Polling Handshake:
   GET /socket.io/?EIO=4&transport=polling&t=PfBUYlW
   Response: 200 OK (returns session ID)

2. WebSocket Upgrade:
   GET /socket.io/?EIO=4&transport=websocket&sid=lFVOEi9OnwREXrmvAlHd
   Response: 101 Switching Protocols

3. Real-time Messages:
   POST /socket.io/?EIO=4&transport=polling&t=PfBUYlS&sid=lFVOEi9OnwREXrmvAlHd
   Body: "40" (Socket.IO protocol message)
```

### 2. Key Parameters

- **EIO=4**: Engine.IO protocol version 4
- **transport**: `polling` (initial) → `websocket` (upgraded)
- **sid**: Session ID (e.g., `lFVOEi9OnwREXrmvAlHd`)
- **t**: Timestamp for cache-busting

### 3. Protocol Messages

The HAR shows message body `"40"` which is Socket.IO protocol format:
- `4` = Engine.IO MESSAGE packet
- `0` = Socket.IO CONNECT packet

---

## How Cell Collective Simulation Works

Based on the screenshot and HAR analysis:

### Real-Time Components

1. **Simulation Graph**: Displays component activity over time
2. **Component States**: Updated in real-time via WebSocket
3. **Simulation Speed**: Controlled by client, synced via Socket.IO
4. **Sliding Window**: Shows last N steps of simulation

### Communication Pattern

```
Client                          Server
  |                               |
  |------ Connect Socket.IO ----->|
  |<----- Session ID (sid) -------|
  |                               |
  |------ Start Simulation ------>|
  |<----- Simulation Step 1 ------|
  |<----- Simulation Step 2 ------|
  |<----- Simulation Step 3 ------|
  |         (continues...)         |
  |                               |
  |------ Stop/Pause ------------>|
  |<----- Confirm Stop ------------|
```

---

## What We've Built So Far

### ✅ Completed

1. **Backend API** (`backend/app.py`):
   - `/api/lesson/<model_id>` - Get lesson data
   - `/api/set-token` - Authentication
   - `/api/profile` - User info
   - `/api/models` - Model listing

2. **Frontend Lesson Interface** (`frontend/lesson.html`):
   - 3-panel layout (instructions, graph, controls)
   - Component list display
   - Control toggles
   - Run/Reset buttons (stubbed)

3. **Token Authentication**:
   - Modal for token input
   - localStorage persistence
   - Backend cookie setting

### ⏸️ NOT Yet Implemented

1. **Socket.IO Client Connection**
2. **Real-time Simulation Execution**
3. **Graph Visualization Updates**
4. **Component State Tracking**
5. **Simulation Controls (speed, pause, reset)**

---

## Next Steps: Adding Real Simulation

To implement real simulation, we need to:

### Option 1: Direct Socket.IO Integration

**Pros**: Full control, real-time updates
**Cons**: Complex, requires Socket.IO library, WebSocket proxy

**Implementation**:
1. Add Socket.IO client library to frontend
2. Create WebSocket proxy in Flask backend
3. Connect to Cell Collective's Socket.IO endpoint
4. Listen for simulation messages
5. Update graph in real-time

**Libraries Needed**:
- Frontend: `socket.io-client.js`
- Backend: `python-socketio`, `flask-socketio`

### Option 2: HTTP Polling (Simpler)

**Pros**: Easier to implement, no WebSocket complexity
**Cons**: Not real-time, higher latency, more bandwidth

**Implementation**:
1. Create `/api/simulation/start/<model_id>` endpoint
2. Poll `/api/simulation/status/<model_id>` every 500ms
3. Return current simulation state
4. Update graph with each poll response

### Option 3: Stub Simulation (Current State)

**Pros**: Immediate demo, no external dependencies
**Cons**: Not real, just for UI testing

**Current Implementation**:
- `startSimulation()` shows "Running..." for 3 seconds
- No actual simulation execution
- No graph updates

---

## Recommendation

For a **kid-friendly prototype**, I recommend:

### Phase 1 (Now): Static Data Demo
- Keep current lesson interface
- Load real model data from API
- Display components and relationships
- Stub simulation buttons with fake progress

### Phase 2 (Next): HTTP Polling Simulation
- Implement basic simulation execution
- Poll for simulation state updates
- Update component states in control panel
- Show simple progress indicator

### Phase 3 (Future): Full Socket.IO Integration
- Add real-time graph updates
- Implement sliding window visualization
- Support pause/resume/speed control
- Match Cell Collective's UX exactly

---

## What You Should Do Next

**Immediate Options**:

1. **Test Current Prototype**:
   - Go to `http://localhost:8000/lesson.html`
   - Enter your token
   - See if model data loads
   - Check if components display correctly

2. **Capture More Data**:
   - Run a longer simulation in Cell Collective
   - Export another HAR with 20-30 steps
   - Look for simulation message payloads

3. **Build HTTP Polling Version**:
   - Simpler than WebSocket
   - Good enough for prototype
   - Can upgrade to Socket.IO later

**Which would you like to try first?**
