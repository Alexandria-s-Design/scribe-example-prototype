# Cell Collective K-12 Wrapper

**Kid-friendly interface for Cell Collective biological simulations**

Transform complex biological simulations into engaging, interactive lessons for K-12 students.

---

## 🎯 Project Goal

Wrap Cell Collective's powerful simulation platform (teach.cellcollective.org) with a simplified, colorful interface designed for elementary and middle school students. Think "biology meets video games" - where complex cellular processes become fun, visual learning experiences.

---

## 🚀 What's Built So Far

### ✅ **Core Architecture (Complete)**

1. **Python API Wrapper** (`cell_collective_api.py`)
   - Reverse-engineered Cell Collective's REST API
   - Cookie-based authentication
   - Model discovery and data fetching
   - Handles 298,000+ biological models

2. **Flask Backend** (`backend/app.py`)
   - Proxies Cell Collective API
   - Handles authentication securely
   - Serves lesson data with proper CORS
   - Ready for production with Gunicorn

3. **3-Panel Lesson Interface** (`frontend/`)
   - Left: Kid-friendly instructions with emojis
   - Center: Interactive graph visualization
   - Right: Component controls (toggle states)
   - Purple gradient theme (approachable for kids)
   - Fully responsive CSS Grid layout

4. **Browser Automation Tools**
   - `extract_cookie_from_browser.py` - Auto-extract session cookies
   - `get_cookie_automatic.py` - Playwright-based cookie capture
   - `get_cookie.bat` - One-click cookie extraction

5. **Authentication System**
   - Token modal for first-time users
   - LocalStorage persistence
   - Automatic token validation
   - Fallback to manual cookie extraction

---

## 📂 Project Structure

```
cell-collective-wrapper/
├── backend/
│   ├── app.py                 # Flask server (port 8000)
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── lesson.html            # Main lesson interface
│   ├── lesson.css             # Styling (purple theme)
│   └── lesson.js              # Client-side logic
├── cell_collective_api.py     # API wrapper
├── test_auth.py               # Authentication testing
├── extract_cookie_from_browser.py  # Cookie extraction
├── get_cookie.bat             # Quick cookie capture
├── README.md                  # This file
├── STATUS.md                  # Current development status
└── NEXT_STEPS.md              # Roadmap
```

---

## 🔧 Quick Start

```bash
# 1. Install dependencies
pip install flask flask-cors requests playwright
playwright install chromium

# 2. Get session cookie (opens browser)
python extract_cookie_from_browser.py

# 3. Start backend
cd backend && python app.py

# 4. Start frontend (new terminal)
cd frontend && npx http-server -p 3000

# 5. Visit http://localhost:3000/lesson.html
```

---

## 🐛 Current Status

**What's Working:**
- ✅ API wrapper successfully authenticates
- ✅ Backend proxies Cell Collective API
- ✅ Frontend displays lesson interface
- ✅ Cookie extraction tools work
- ✅ 3-panel layout renders correctly

**What's In Progress:**
- 🔧 Verifying fresh cookies load model data
- 🔧 Graph visualization needs real data
- 🔧 Component toggles not connected yet

**See STATUS.md for detailed info**

---

## 🎓 Built By

**Alexandria's Design** - Transforming education for the Fourth Industrial Revolution

**Let's get to the bread.** 💰
