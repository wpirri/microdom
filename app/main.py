from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.routers import cgi_bin
from app.log_utils import get_daily_logger

app = FastAPI(
    title="Microservicio comunicacion con dispositivos de domotica",
    version="1.0.0"
)

app.include_router(cgi_bin.router)

@app.get("/")
def get_root():
    return {"message": "Microservicio de Domotica 1.0.0.0"}

@app.get("/health")
def healt():
    return {"status": "ok"}
