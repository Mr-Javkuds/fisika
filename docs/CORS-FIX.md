# ⚠️ CORS Error - Quick Fix Guide

## 🔴 Problem
Sections failed to load because you opened `index.html` directly (double-click).

**Error**: Browser blocks `fetch()` for local files due to CORS security policy.

---

## ✅ Solution: Use Web Server

### 🎯 **Option 1: One-Click Launcher** (EASIEST!)

**Double-click this file:**
```
start-server.bat
```

Then open browser to: `http://localhost:8000`

---

### 🎯 **Option 2: Manual Server**

```bash
cd docs
python -m http.server 8000
```

Then open: `http://localhost:8000`

---

### 🎯 **Option 3: VS Code Live Server**

1. Install VS Code extension: "Live Server"
2. Right-click `docs/index.html`
3. Select "Open with Live Server"

---

## 🔄 Alternative: Use Monolithic Version

If you **really** need to open without server:

```bash
# Restore old monolithic version (works with file://)
copy docs\index.html.backup docs\index.html
```

**Trade-off**: 
- ✅ Works with double-click
- ❌ Lost modular benefits (back to 3098 lines)

---

## 💡 Why This Happens

```
file:///path/to/index.html
  ↓ tries to fetch()
file:///path/to/sections/data_types.html
  ❌ BLOCKED by browser CORS policy
```

**Web server fixes this:**
```
http://localhost:8000/index.html
  ↓ fetch()
http://localhost:8000/sections/data_types.html
  ✅ ALLOWED (same origin)
```

---

## ✅ Recommended Workflow

**Development**: 
- Use `start-server.bat` or Live Server
- Edit sections in `docs/sections/`
- Refresh browser to see changes

**Production**: 
- Deploy to real web server (GitHub Pages, Netlify, etc.)
- Modules load perfectly

---

**Quick Fix**: Just run `start-server.bat` and you're good to go! 🚀
