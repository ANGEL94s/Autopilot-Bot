"""
Entrypoint for python -m autopilot
Runs the async main() in autopilot.app
"""
import asyncio
import logging
import sys
import signal

from .app import main

def handle_shutdown(signum, frame):
    """Handle shutdown signals gracefully."""
    logging.info(f"Received signal {signum}, initiating graceful shutdown...")
    sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Register signal handlers for Railway
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)
    
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception("Fatal error while running AUTOPILOT: %s", e)
        sys.exit(1)
