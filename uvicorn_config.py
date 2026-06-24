"""
Uvicorn configuration for NetSentinel API
"""

import os

# Server
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8000))
reload = os.getenv("RELOAD", "True").lower() == "true"
workers = int(os.getenv("WORKERS", 1))

# Logging
log_level = os.getenv("LOG_LEVEL", "info")

# SSL
ssl_keyfile = os.getenv("SSL_KEYFILE")
ssl_certfile = os.getenv("SSL_CERTFILE")

# Application
app = "main:app"
