#!/usr/bin/env python3
"""
Simple HTTP server with auto-reload for the database visualization dashboard.
Automatically regenerates the dashboard when database changes are detected.
"""

import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys

PORT = 8000
BASE_DIR = Path(__file__).parent.parent

class DashboardHandler(FileSystemEventHandler):
    """Handler for file system events"""
    def __init__(self):
        self.last_modified = {}
    
    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return
        
        # Check if database file changed
        if event.src_path.endswith('broadcast_industry.db'):
            print("\n[INFO] Database changed, regenerating dashboard...")
            self.regenerate_dashboard()
    
    def regenerate_dashboard(self):
        """Regenerate the HTML dashboard"""
        try:
            result = subprocess.run(
                [sys.executable, str(BASE_DIR / "scripts" / "generate_database_visualization.py")],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR)
            )
            if result.returncode == 0:
                print("[SUCCESS] Dashboard regenerated successfully!")
            else:
                print(f"[ERROR] Failed to regenerate dashboard: {result.stderr}")
        except Exception as e:
            print(f"[ERROR] Exception during regeneration: {e}")

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler with better logging"""
    def log_message(self, format, *args):
        """Override to show cleaner logs"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_file_watcher():
    """Start watching for file changes"""
    event_handler = DashboardHandler()
    observer = Observer()
    observer.schedule(event_handler, str(BASE_DIR), recursive=False)
    observer.start()
    print(f"[INFO] File watcher started. Monitoring: {BASE_DIR}")
    return observer

def main():
    """Start the HTTP server"""
    os.chdir(BASE_DIR)
    
    # Check if dashboard exists, generate if not
    dashboard_path = BASE_DIR / "database_visualization.html"
    if not dashboard_path.exists():
        print("[INFO] Dashboard not found, generating...")
        subprocess.run(
            [sys.executable, str(BASE_DIR / "scripts" / "generate_database_visualization.py")],
            cwd=str(BASE_DIR)
        )
    
    # Start file watcher
    observer = start_file_watcher()
    
    # Start HTTP server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/database_visualization.html"
        print(f"\n{'='*60}")
        print(f"🚀 Dashboard Server Running")
        print(f"{'='*60}")
        print(f"📊 Open in browser: {url}")
        print(f"📁 Serving from: {BASE_DIR}")
        print(f"🔄 Auto-reload: Enabled (watches database changes)")
        print(f"{'='*60}")
        print(f"\nPress Ctrl+C to stop the server\n")
        
        # Open browser automatically
        try:
            webbrowser.open(url)
        except:
            print(f"Could not open browser automatically. Please visit: {url}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down server...")
            observer.stop()
            observer.join()
            print("[INFO] Server stopped.")

if __name__ == "__main__":
    import os
    main()
