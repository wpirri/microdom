from fastapi import FastAPI
from app.routers import healt
from app.routers import cgi_bin
from app.config_utils import get_config_value
from app.log_utils import get_daily_logger

logger = get_daily_logger("microdom", "/app/logs/microdom.log")

app = FastAPI(
    title="Microservicio comunicacion con dispositivos de domotica",
    version="1.0.0"
)

app.include_router(healt.router)
app.include_router(cgi_bin.router)

@app.get("/")
def get_root():
    logger.info("Petición recibida en /")
    return {"message": "Microservicio de Domotica"}

