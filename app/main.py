from fastapi import FastAPI, APIRouter
import os
import subprocess
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

@api_router.post("/vibrate_on", status_code=201)
def vibrate_on() -> dict:
    """
    Turn vibrate On
    """
    logger.info("Turn vibrate on")
    subprocess.run(["gpio", "write", "22", "1"])
    subprocess.run(["gpio", "write", "24", "0"])
    return {"msg": "vibrate on"}

@api_router.post("/vibrate_off", status_code=201)
def vibrate_off() -> dict:
    """
    Turn vibrate off
    """
    logger.info("Turn vibrate off")
    subprocess.run(["gpio", "write", "22", "0"])
    subprocess.run(["gpio", "write", "24", "0"])
    return {"msg": "vibrate off"}

@api_router.post("/on", status_code=201)
def on() -> dict:
    """
    Turn On
    """
    logger.info("Turn on")
    subprocess.run(["gpio", "write", "21", "1"])
    subprocess.run(["gpio", "write", "25", "0"])
    subprocess.run(["gpio", "write", "22", "1"])
    subprocess.run(["gpio", "write", "24", "0"])
    return {"msg": "on"}

@api_router.post("/off", status_code=201)
def off() -> dict:
    """
    Turn off
    """
    logger.info("Turn off")
    subprocess.run(["gpio", "write", "21", "0"])
    subprocess.run(["gpio", "write", "25", "0"])
    subprocess.run(["gpio", "write", "22", "0"])
    subprocess.run(["gpio", "write", "24", "0"])
    return {"msg": "off"}

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info("start")
    subprocess.run(["gpio", "mode", "25", "out"])
    subprocess.run(["gpio", "mode", "21", "out"])
    subprocess.run(["gpio", "mode", "22", "out"])
    subprocess.run(["gpio", "mode", "24", "out"])
    subprocess.run(["gpio", "write", "21", "0"])
    subprocess.run(["gpio", "write", "25", "0"])
    subprocess.run(["gpio", "write", "22", "0"])
    subprocess.run(["gpio", "write", "24", "0"])


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("shutdown")
    subprocess.run(["gpio", "write", "21", "0"])
    subprocess.run(["gpio", "write", "25", "0"])
    subprocess.run(["gpio", "write", "22", "0"])
    subprocess.run(["gpio", "write", "24", "0"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")