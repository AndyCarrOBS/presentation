# Running the Dashboard Server

## Quick Start

The dashboard needs to run on a web server (not `file://`) for the D3.js network graph to work properly due to browser security restrictions.

### Simple Server (No Dependencies)

```bash
python3 scripts/serve_dashboard_simple.py
```

This will:
- Start a web server on `http://localhost:8000`
- Automatically open the dashboard in your browser
- Serve the dashboard with proper CORS headers

### Access the Dashboard

Once the server is running, open:
```
http://localhost:8000/database_visualization.html
```

## Alternative: Python's Built-in Server

If the simple server script doesn't work, you can use Python's built-in HTTP server:

```bash
cd /home/andycarr/code/business-dev/presentation
python3 -m http.server 8000
```

Then open: `http://localhost:8000/database_visualization.html`

## Troubleshooting

### Network Graph Not Showing

1. **Check browser console** (F12) for JavaScript errors
2. **Verify D3.js is loading**: Look for errors about `d3` being undefined
3. **Check internet connection**: D3.js loads from CDN
4. **Try a different browser**: Some browsers have stricter security

### Server Won't Start

1. **Port already in use**: Change port in the script (default: 8000)
2. **Permission denied**: Make sure you have write access to the directory
3. **Python version**: Requires Python 3.6+

### Dashboard Not Updating

After making database changes:
```bash
python3 scripts/generate_database_visualization.py
```

Then refresh the browser (or the server will serve the updated file automatically).

## Features That Work

✅ All charts (Chart.js)
✅ Tables and search
✅ Statistics
✅ Network graph (when served via HTTP)

## Network Graph Details

The interactive network graph uses:
- **D3.js v7** (loaded from CDN)
- **Force-directed layout** for automatic positioning
- **Click and drag** to rearrange nodes
- **Hover** for tooltips

If the graph doesn't appear:
1. Check browser console for errors
2. Ensure you're accessing via `http://` not `file://`
3. Verify D3.js loaded (check Network tab in browser dev tools)
