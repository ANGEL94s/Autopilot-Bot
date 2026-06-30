"""
Entrypoint for python -m autopilot
Runs the async main() in autopilot.app
"""
import asyncio
import logging
import sys

from .app import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception("Fatal error while running AUTOPILOT: %s", e)
        sys.exit(1)
