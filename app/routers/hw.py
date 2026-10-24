from fastapi import APIRouter, Request, Form
from fastapi.concurrency import run_in_threadpool
from app.log_utils import get_daily_logger
from app.hw_utils import get_touch_download_list, get_touch_download_screen, add_invalid_hardware, check_hw
from app.dom_utils import analyze_event, get_hw_io_status, get_hw_update_data, update_assign_state, update_assign_states_bulk, change_assign_by_name

logger = get_daily_logger()

router = APIRouter(prefix="/hw", tags=["hw"])
# 2026-04-04 03:12:36,583 - INFO - [infoio.cgi] 
# FORM={'ID': 'c8c9a34a61af', 'TYP': 'IO', 'IO1': '0', 'IO2': '0', 'IO3': '0', 'IO4': '1', 'IO5': '0', 'IO6': '0', 
#       'OUT1': '0', 'OUT2': '0', 'OUT3': '0', 'OUT4': '1', 
#       'CHG': 'IO1', 'ONLINE': '1', 
#       'AT': '1.7.3.0(Mar 19 2020 18:15:04)', 'SDK': '3.0.3(8427744)', 'FW': 'Feb  6 2026 12:28:06'}
@router.post("/infoio")
@router.post("/infoio.cgi")
async def infoio(request: Request):
    raddr = request.client.host if request.client else "0.0.0.0"
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    return await run_in_threadpool(_process_infoio, data, raddr)

def _process_infoio(data: dict, raddr: str):
    # Información del dispositivo
    hw_mac_addr = data.get("ID", "NULL").upper()
    hw_typ = data.get("TYP", None)
    FW = data.get("FW", None)
    AT = data.get("AT", None)
    SDK = data.get("SDK", None)

    # Busco el dispositivo por MAC
    Dispositivo = check_hw(hw_mac_addr, raddr, f"FW:{FW} AT:{AT} SDK:{SDK}")
    if Dispositivo:
        OFFLINE = data.get("OFFLINE", None)
        if OFFLINE:
            logger.info(f"HW: {Dispositivo} estuvo OFFLINE (Firmware: {FW})")
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
            CARD = data.get("CARD", None)
            UPDATEIO = data.get("UPDATEIO", None)

            analyze_event(hw_mac_addr, CHG, 
                          IO1, IO2, IO3, IO4, IO5, IO6, IO7, IO8, 
                          OUT1, OUT2, OUT3, OUT4, OUT5, OUT6, OUT7, OUT8, CARD)

            update_assign_states_bulk(hw_mac_addr, {
                "IO1": IO1, "IO2": IO2, "IO3": IO3, "IO4": IO4,
                "IO5": IO5, "IO6": IO6, "IO7": IO7, "IO8": IO8
            })

            return {get_hw_io_status(hw_mac_addr) + get_hw_update_data(hw_mac_addr, UPDATEIO)}
        elif hw_typ == "TOUCH":
            return {"error=0&message=Ok" + get_hw_update_data(hw_mac_addr)}
        else:
            logger.info(f"HW: {hw_mac_addr} tipo desconocido {hw_typ}")
            return {f"error=3&message=HW {hw_mac_addr} tipo desconocido {hw_typ}"}
    else:
        add_invalid_hardware(hw_mac_addr)
        return {f"error=2&message=HW {hw_mac_addr} no encontrado"}

@router.get("/switch")
def switch(request: Request):
    request_params = dict(request.query_params)
    objeto = request_params.get("Objeto", None)
    change_assign_by_name(objeto, 3)
    return {"error=0&message=Ok"}

@router.get("/pulse")
def pulse(request: Request):
    request_params = dict(request.query_params)
    objeto = request_params.get("Objeto", None)
    s = request_params.get("Segundos", None)
    change_assign_by_name(objeto, 4, s)
    return {"error=0&message=Ok"}

### Configuracion de HW
@router.get("/hwconfig")
async def hwconfig_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    screen = request_params.get("screen", None)
    if screen:
        return get_touch_download_screen(request.client.host, screen)
    else:
        return get_touch_download_list(request.client.host)

@router.post("/hwconfig")
async def hwconfig_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    if funcion:
        logger.info(f"[hwconfig] Funcion: {funcion}")

    return {f"error=0&message=Ok"}

