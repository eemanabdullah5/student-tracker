from fastapi import FastAPI

from app.routes import health

app = FastAPI(title="Student Assignment & Progress Tracker")

app.include_router(health.router)
