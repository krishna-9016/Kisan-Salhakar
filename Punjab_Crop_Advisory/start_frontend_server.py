#!/usr/bin/env python3
"""
Simple HTTP Server for Frontend
===============================
Serves the simple_frontend.html to avoid CORS issues when connecting to API
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 6060
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    print("🌐 Punjab Crop Advisory - Frontend Server")
    print("=" * 45)
    print(f"📁 Serving directory: {DIRECTORY}")
    print(f"🔗 Server URL: http://localhost:{PORT}")
    print(f"🎯 Frontend URL: http://localhost:{PORT}/simple_frontend.html")
    print(f"🚀 API Server: http://localhost:9090")
    print("=" * 45)
    
    # Check if simple_frontend.html exists
    frontend_file = Path(DIRECTORY) / "simple_frontend.html"
    if not frontend_file.exists():
        print("❌ Error: simple_frontend.html not found!")
        print(f"   Expected location: {frontend_file}")
        return
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"✅ Server starting on port {PORT}...")
            print(f"🌐 Open: http://localhost:{PORT}/simple_frontend.html")
            print("Press Ctrl+C to stop the server")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f"http://localhost:{PORT}/simple_frontend.html")
                print("🔍 Browser opened automatically!")
            except:
                print("💡 Please open the URL manually in your browser")
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"❌ Error: Port {PORT} is already in use!")
            print("   Try stopping other servers or use a different port")
        else:
            print(f"❌ Error starting server: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    main()
