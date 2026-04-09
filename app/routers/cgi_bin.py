from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.dom_utils import check_hw, analyze_event, get_hw_io_status

logger = get_daily_logger()

router = APIRouter(prefix="/cgi-bin", tags=["cgi"])
# 2026-04-04 03:12:36,583 - INFO - [infoio.cgi] 
# FORM={'ID': 'c8c9a34a61af', 'TYP': 'IO', 'IO1': '0', 'IO2': '0', 'IO3': '0', 'IO4': '1', 'IO5': '0', 'IO6': '0', 
#       'OUT1': '0', 'OUT2': '0', 'OUT3': '0', 'OUT4': '1', 
#       'CHG': 'IO1', 'ONLINE': '1', 
#       'AT': '1.7.3.0(Mar 19 2020 18:15:04)', 'SDK': '3.0.3(8427744)', 'FW': 'Feb  6 2026 12:28:06'}
@router.post("/infoio.cgi")
async def infoio(request: Request):
    raddr = request.client.host
    # 1. Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    #logger.info(f"[infoio.cgi] FORM={data}")
    hw_mac_addr = data.get("ID", "NULL").upper()
    hw_typ = data.get("TYP", None)

    #ONLINE = data.get("ONLINE", None)
    OFFLINE = data.get("OFFLINE", None)
    AT = data.get("AT", None)
    SDK = data.get("SDK", None)
    FW = data.get("FW", None)

    # 2. Leer parámetros GET (query string)
    request_params = dict(request.query_params)
    #logger.info("[infoio.cgi] GET params: %s", request_params)

    # 3. Leer headers (variables del navegador)
    headers = dict(request.headers)
    #logger.info("[infoio.cgi] Headers: %s", headers)

    # Busco el dispositivo por MAC
    rc = check_hw(hw_mac_addr, raddr, f"AT:{AT} SDK:{SDK} FW:{FW}")
    if rc:
        if hw_typ == "IO":
            IO1 = data.get("IO1", None)
            IO2 = data.get("IO2", None)
            IO3 = data.get("IO3", None)
            IO4 = data.get("IO4", None)
            IO5 = data.get("IO5", None)
            IO6 = data.get("IO6", None)
            IO7 = data.get("IO7", None)
            IO8 = data.get("IO8", None)
            OUT1 = data.get("OUT1", None)
            OUT2 = data.get("OUT2", None)
            OUT3 = data.get("OUT3", None)
            OUT4 = data.get("OUT4", None)
            OUT5 = data.get("OUT5", None)
            OUT6 = data.get("OUT6", None)
            OUT7 = data.get("OUT7", None)
            OUT8 = data.get("OUT8", None)
            CHG = data.get("CHG", None)

            analyze_event(hw_mac_addr, CHG, IO1, IO2, IO3, IO4, IO5, IO6, IO7, IO8, OUT1, OUT2, OUT3, OUT4, OUT5, OUT6, OUT7, OUT8)


            return get_hw_io_status(hw_mac_addr)
        else:
            if hw_typ == "TOUCH":

                return {"error=0&message=Ok"}
            else:
                logger.info(f"HW: {hw_mac_addr} tipo desconocido {hw_typ}")
                return {f"error=3&message=HW {hw_mac_addr} tipo desconocido {hw_typ}"}
    else:
        logger.info(f"HW: {hw_mac_addr} no encontrado")
        return {f"error=2&message=HW {hw_mac_addr} no encontrado"}


@router.get("/abmassign.cgi")
async def abmassign(request: Request):
    raddr = request.client.host
    # 1. Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    logger.info(f"[abmassign.cgi] FORM={data}")

    # 2. Leer parámetros GET (query string)
    request_params = dict(request.query_params)
    logger.info("[abmassign.cgi] GET params: %s", request_params)

    # 3. Leer headers (variables del navegador)
    headers = dict(request.headers)
    logger.info("[abmassign.cgi] Headers: %s", headers)
    # Busco el dispositivo por IP
    rc = check_hw(None, raddr, 'completar')
    if rc:
        logger.info("Periférico encontrado")



        
        return {"error=0&message=Ok"}
    else:
        logger.info(f"Periférico {raddr} no encontrado")
        return {f"error=2&message=HW {raddr} no encontrado"}
