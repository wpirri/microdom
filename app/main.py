from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.log_utils import get_daily_logger

from app.routers import cgi_bin, download, hw

app = FastAPI(
    title="Microservicio comunicacion con dispositivos de domotica",
    version="1.0.0"
)

logger = get_daily_logger()

# Routers existentes
app.include_router(cgi_bin.router)
app.include_router(download.router)
app.include_router(hw.router)

@app.get("/health")
def health():
    return {"status": "ok"}
