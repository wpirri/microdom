from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.dom_utils import analyze_event, get_hw_io_status, get_assign_status_id, get_assign_info_id
from app.abm.abm_hw import check_hw, get_hardware_list, get_hardware, add_hardware, update_hardware, delete_hardware
from app.abm.abm_sys import add_sys_config, get_sys_config
from app.abm.abm_assign import add_assign, get_assign_list, get_assign, update_assign, delete_assign, change_assign_by_name
from app.abm.abm_event import add_event, get_event_list, get_event, update_event, delete_event
from app.abm.abm_group import add_group, get_group_list, get_group, update_group, delete_group
from app.abm.abm_user import add_user, get_user_list, get_user, update_user, delete_user

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
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    # Información del dispositivo
    hw_mac_addr = data.get("ID", "NULL").upper()
    hw_typ = data.get("TYP", None)
    AT = data.get("AT", None)
    SDK = data.get("SDK", None)
    FW = data.get("FW", None)
    # Si el dice que estuvo offline
    OFFLINE = data.get("OFFLINE", None)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Leer headers (variables del navegador)
    headers = dict(request.headers)

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

### ABM de la configuración del sistema
@router.get("/abmsys.cgi")
async def abmsys_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    if funcion:
        logger.info(f"[abmsys.cgi] Funcion: {funcion}")
        if funcion == "get_current":
            return get_sys_config()
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}

@router.post("/abmsys.cgi")
async def abmsys_post(request: Request):
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
        logger.info(f"[abmsys.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_sys_config(data)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}

### ABM HW
@router.get("/abmhw.cgi")
async def abmhw_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    id = request_params.get("Id", 0)
    if funcion:
        logger.info(f"[abmhw.cgi] Funcion: abmhw/{funcion}")
        if funcion == "get":
            return get_hardware(id)
        elif funcion == "delete":
            return delete_hardware(id)
        else:
            return {f"error=99&message=Función: {funcion} no implementadad aún"}
    else:
        return get_hardware_list()

@router.post("/abmhw.cgi")
async def abmhw_post(request: Request):
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
        logger.info(f"[abmhw.cgi] Funcion: abmhw/{funcion}")
        if funcion == "add":
            return add_hardware(data)
        elif funcion == "update":
            return update_hardware(data)
        else:
            return {f"error=99&message=Función: {funcion} no implementadad aún"}
    else:
        return {f"error=99&message=Función: no informada"}

### ABM Assign
@router.get("/abmassign.cgi")
async def abmassign_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)
    
    # Me abro por función
    funcion = request_params.get("funcion", None)
    if funcion:
        logger.info(f"[abmassign.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        planta = request_params.get("Planta", None)
        objeto = request_params.get("Objeto", None)
        if funcion == "status":
            return get_assign_status_id(id, planta)
        elif funcion == "info":
            return get_assign_info_id(id, planta)
        elif funcion == "switch":
            change_assign_by_name(objeto, 3)
            return {"error=0&message=Ok"}
        elif funcion == "on":
            change_assign_by_name(objeto, 1)
            return {"error=0&message=Ok"}
        elif funcion == "off":
            change_assign_by_name(objeto, 2)
            return {"error=0&message=Ok"}
        elif funcion == "get":
            return get_assign(id)
        elif funcion == "delete":
            return delete_assign(id)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return get_assign_list()

@router.post("/abmassign.cgi")
async def abmassign_post(request: Request):
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
        logger.info(f"[abmassign.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_assign(data)
        elif funcion == "update":
            return update_assign(data)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}

### ABM Event
@router.get("/abmev.cgi")
async def abmevent_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    if funcion:
        logger.info(f"[abmev.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_event(id)
        elif funcion == "delete":
            return delete_event(id)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return get_event_list()
    
@router.post("/abmev.cgi")
async def abmevent_post(request: Request):
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
        logger.info(f"[abmev.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_event(data)
        elif funcion == "update":
            return update_event(data)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}
    
### ABM Group
@router.get("/abmgroup.cgi")
async def abmgroup_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    if funcion:
        logger.info(f"[abmgroup.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_group(id)
        elif funcion == "delete":
            return delete_group(id)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return get_group_list()
    
@router.post("/abmgroup.cgi")
async def abmgroup_post(request: Request):
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
        logger.info(f"[abmgroup.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_group(data)
        elif funcion == "update":
            return update_group(data)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}
    
### ABM User
@router.get("/abmuser.cgi")
async def abmuser_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    if funcion:
        logger.info(f"[abmuser.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_user(id)
        elif funcion == "delete":
            return delete_user(id)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return get_user_list()
    
@router.post("/abmuser.cgi")
async def abmuser_post(request: Request):
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
        logger.info(f"[abmuser.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_user(data)
        elif funcion == "update":
            return update_user(data)
        else:
            logger.info(f"Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}
    

    
