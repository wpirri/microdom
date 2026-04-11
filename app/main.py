from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.log_utils import get_daily_logger

from app.routers import cgi_bin, download

app = FastAPI(
    title="Microservicio comunicacion con dispositivos de domotica",
    version="1.0.0"
)

logger = get_daily_logger()

# Routers existentes
app.include_router(cgi_bin.router)
app.include_router(download.router)

# Archivos estáticos específicos
app.mount("/css", StaticFiles(directory="/app/html/css"), name="css")
app.mount("/js", StaticFiles(directory="/app/html/js"), name="js")
app.mount("/images", StaticFiles(directory="/app/html/images"), name="images")

BASE_DIR = Path("/app/html")  # Cambialo según tu mapeo real

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def index():
    file_path = BASE_DIR / "index.html"
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(file_path)

@app.get("/{filename}", response_class=HTMLResponse)
def root(filename: str):
    file_path = BASE_DIR / filename
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(file_path)

@app.get("/data/{filename}", response_class=HTMLResponse)
def root(filename: str):
    file_path = BASE_DIR / "data" / filename
    # Validar existencia
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(file_path)
