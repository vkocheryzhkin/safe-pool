from fastapi import FastAPI, APIRouter
import OPi.GPIO as GPIO
import logging
from logging.config import dictConfig
from app.log_config import log_config

dictConfig(log_config)

app = FastAPI(
    title="Safe Swimming Pool  API", openapi_url="/openapi.json"
)

logger = logging.getLogger("uvicorn")
api_router = APIRouter()

@api_router.get("/", status_code=200)
def health() -> dict:
    """
    Health check
    """
    return {"health": "ok"}

@api_router.post("/on", status_code=201)
def on() -> dict:
    """
    Turn On
    """
    logger.info("Turn on")
    GPIO.output(5, 1)
    return {"msg": "on"}

@api_router.post("/off", status_code=201)
def off() -> dict:
    """
    Turn off
    """
    logger.info("Turn off")
    GPIO.output(5, 0)
    return {"msg": "off"}

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info("start")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("shutdown")
    GPIO.cleanup()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")