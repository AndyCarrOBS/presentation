#!/usr/bin/env python3
"""
Simple HTTP server for the database visualization dashboard.
No external dependencies - uses only Python standard library.
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path
import sys

PORT = 8000
BASE_DIR = Path(__file__).parent.parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler with better logging and CORS headers"""
    
    def end_headers(self):
        """Add CORS headers to allow cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Override to show cleaner logs"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    """Start the HTTP server"""
    os.chdir(BASE_DIR)
    
    # Check if dashboard exists
    dashboard_path = BASE_DIR / "database_visualization.html"
    if not dashboard_path.exists():
        print("[WARNING] Dashboard not found. Generating...")
        try:
            subprocess.run(
                [sys.executable, str(BASE_DIR / "scripts" / "generate_database_visualization.py")],
                cwd=str(BASE_DIR),
                check=True
            )
            print("[SUCCESS] Dashboard generated!")
        except Exception as e:
            print(f"[ERROR] Could not generate dashboard: {e}")
            print("Please run: python3 scripts/generate_database_visualization.py")
            return
    
    # Start HTTP server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/database_visualization.html"
        print(f"\n{'='*60}")
        print(f"🚀 Dashboard Server Running")
        print(f"{'='*60}")
        print(f"📊 Open in browser: {url}")
        print(f"📁 Serving from: {BASE_DIR}")
        print(f"💡 Tip: Edit database and regenerate dashboard manually")
        print(f"   python3 scripts/generate_database_visualization.py")
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
            print("[INFO] Server stopped.")

if __name__ == "__main__":
    import subprocess
    main()
