from fastapi import APIRouter, Request, Form
from logging_config import get_daily_logger

logger = get_daily_logger("microdom", "/app/logs/microdom.log")

router = APIRouter(prefix="/cgi-bin", tags=["cgi"])

@router.post("/infoio.cgi")
async def infoio(request: Request):
    # 1. Leer el cuerpo RAW del POST
    #body_bytes = await request.body()
    #body = body_bytes.decode(errors="ignore")
    #logger.info("[infoio.cgi] POST RAW: %s", body)

    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    logger.info(f"[infoio.cgi] FORM={data}")

    # 2. Leer parámetros GET (query string)
    query_params = dict(request.query_params)
    logger.info("[infoio.cgi] GET params: %s", query_params)

    # 3. Leer headers (variables del navegador)
    headers = dict(request.headers)
    logger.info("[infoio.cgi] Headers: %s", headers)

    return {"error=0&message=infoio endpoint reached"}
