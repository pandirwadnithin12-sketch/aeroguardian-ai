"""
AeroGuardian AI - Single-Command Launcher
Launches Starlette ASGI server with Uvicorn and opens React frontend in default browser.
"""

import os
import sys
import time
import webbrowser
import threading
import uvicorn

def open_browser(url: str):
    """Wait 1.5s for server to start, then open browser."""
    time.sleep(1.5)
    print(f">> Opening AeroGuardian AI in browser: {url}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")

def main():
    print("=" * 60)
    print("[AEROGUARDIAN AI] PILOT WORKLOAD & DECISION SUPPORT")
    print("Theme: 'Smart Systems for a Safer Future in Aviation'")
    print("=" * 60)
    print(">> React UI & Starlette REST API Backend Starting...")
    print(">> URL: http://localhost:8000")
    print("=" * 60)

    # Spawn browser thread
    threading.Thread(target=open_browser, args=("http://localhost:8000",), daemon=True).start()

    # Run Uvicorn ASGI server
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    main()
