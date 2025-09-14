from fastapi import FastAPI
from app.config import settings
from app.routes import router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

# Routes
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.VERSION}
