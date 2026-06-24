#!/usr/bin/env python3
"""
NetSentinel Startup Script
"""

import sys
import os
from pathlib import Path
import uvicorn

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Change to backend directory
os.chdir(backend_path)

if __name__ == "__main__":

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info")

    print(f"""
╔════════════════════════════════════════════════════╗
║    NetSentinel - Network Threat Visualizer        ║
║    Starting API Server...                         ║
╚════════════════════════════════════════════════════╝

Host: {host}
Port: {port}
Reload: {reload}
Log Level: {log_level}
""")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level
    )