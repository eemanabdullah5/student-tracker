import logging

from fastapi import FastAPI

from app.core.logging import setup_logging
from app.routes import health

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Student Assignment & Progress Tracker")

app.include_router(health.router)

logger.info("Application configured")
