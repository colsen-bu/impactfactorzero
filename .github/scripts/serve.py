#!/usr/bin/env python3
"""
Simple local development server for the static blog.
Serves the blog files locally for preview and development.
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

# Default port for the development server
DEFAULT_PORT = 8000

class BlogHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the blog server."""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve from (the blog root)
        # Handle both locations: scripts/serve.py and .github/scripts/serve.py
        current_file = Path(__file__).resolve()
        if '.github' in current_file.parts:
            # If in .github/scripts/, go up two levels to reach repo root
            blog_root = current_file.parent.parent.parent
        else:
            # If in scripts/, go up one level to reach repo root
            blog_root = current_file.parent.parent
        os.chdir(blog_root)
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Override to provide cleaner log messages."""
        print(f"[{self.address_string()}] {format % args}")

def main():
    """Start the development server."""
    port = DEFAULT_PORT
    
    # Check for port argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print(f"Using default port: {DEFAULT_PORT}")
            port = DEFAULT_PORT
    
    # Check if port is available
    try:
        with socketserver.TCPServer(("", port), BlogHTTPRequestHandler) as httpd:
            blog_url = f"http://localhost:{port}"
            
            print("=" * 50)
            print("🚀 Static Blog Development Server")
            print("=" * 50)
            print(f"📡 Server running at: {blog_url}")
            print(f"📁 Serving from: {Path.cwd()}")
            print("=" * 50)
            print("📝 Available pages:")
            print(f"   • Home: {blog_url}")
            print(f"   • About: {blog_url}/about.html")
            print(f"   • Editor: {blog_url}/editor.html")
            print("=" * 50)
            print("💡 Tips:")
            print("   • Edit markdown files in drafts/")
            print("   • Use the web editor at /editor.html")
            print("   • Push to GitHub to auto-publish")
            print("   • Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Open browser automatically
            try:
                webbrowser.open(blog_url)
                print(f"🌐 Opening {blog_url} in your default browser...")
            except Exception:
                print("🌐 Please open your browser and navigate to the URL above")
            
            print("\n✅ Server started successfully!")
            print("   Watching for file changes... (manual refresh needed)")
            
            # Start serving
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {port} is already in use.")
            print(f"   Try a different port: python scripts/serve.py {port + 1}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Thanks for developing!")
        sys.exit(0)

if __name__ == "__main__":
    main()