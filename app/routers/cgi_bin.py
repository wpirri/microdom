from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.dom_utils import analyze_event, get_hw_io_status, get_assign_status_id, get_assign_info_id, get_hw_update_data
from app.abm.abm_hw import check_hw, get_hardware_list, get_hardware, add_hardware, get_hardware_list_all, update_hardware, delete_hardware, set_hardware_update_flag
from app.abm.abm_sys import add_sys_config, get_sys_config
from app.abm.abm_assign import add_assign, get_assign_list, get_assign, get_assign_list_all, update_assign, delete_assign, change_assign_by_name, add_assign_to_planta
from app.abm.abm_event import add_event, get_event_list, get_event_list_all, get_event, update_event, delete_event
from app.abm.abm_group import add_group, get_group_list, get_group_list_all, get_group, get_group_list_all, update_group, delete_group
from app.abm.abm_user import add_user, get_user_list, get_user, get_user_list_all, update_user, delete_user
from app.abm.abm_at import get_task_list, get_task_list_all, add_task, get_task, update_task, delete_task
from app.abm.abm_auto import get_auto_list, get_auto_list_all, add_auto, get_auto, update_auto, delete_auto
from app.abm.abm_touch import add_touch, delete_touch, get_touch, get_touch_list, get_touch_list_all, update_touch
from app.hw_utils import get_touch_download_list, get_touch_download_screen

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
    FW = data.get("FW", None)
    AT = data.get("AT", None)
    SDK = data.get("SDK", None)
    # Si el dice que estuvo offline
    OFFLINE = data.get("OFFLINE", None)
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Leer headers (variables del navegador)
    headers = dict(request.headers)

    # Busco el dispositivo por MAC
    rc = check_hw(hw_mac_addr, raddr, f"FW:{FW} AT:{AT} SDK:{SDK}")
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
            CARD = data.get("CARD", None)

            analyze_event(hw_mac_addr, CHG, 
                          IO1, IO2, IO3, IO4, IO5, IO6, IO7, IO8, 
                          OUT1, OUT2, OUT3, OUT4, OUT5, OUT6, OUT7, OUT8, CARD)

            return {get_hw_io_status(hw_mac_addr) + get_hw_update_data(hw_mac_addr)}
        elif hw_typ == "TOUCH":
            return {"error=0&message=Ok" + get_hw_update_data(hw_mac_addr)}
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
        #logger.info(f"[abmsys.cgi] Funcion: {funcion}")
        if funcion == "get_current":
            return get_sys_config()
        else:
            logger.info(f"[GET abmsys] Función desconocida: {funcion}")
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
        #logger.info(f"[abmsys.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_sys_config(data)
        else:
            logger.info(f"[POST abmsys] Función desconocida: {funcion}")
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
        #logger.info(f"[abmhw.cgi] Funcion: abmhw/{funcion}")
        if funcion == "get":
            return get_hardware(id)
        elif funcion == "delete":
            return delete_hardware(id)
        elif funcion == "list":
            return get_hardware_list()
        elif funcion == "listall":
            return get_hardware_list_all()
        elif funcion == "update_firmware":
            return set_hardware_update_flag(id, 1, 0, 0)
        elif funcion == "update_wifi":
            return set_hardware_update_flag(id, 0, 1, 0)
        elif funcion == "update_ioconfig":
            return set_hardware_update_flag(id, 0, 0, 1)
        else:
            logger.info(f"[GET abmhw] Función desconocida: {funcion}")
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
        #logger.info(f"[abmhw.cgi] Funcion: abmhw/{funcion}")
        if funcion == "add":
            return add_hardware(data)
        elif funcion == "update":
            return update_hardware(data)
        else:
            logger.info(f"[POST abmhw] Función desconocida: {funcion}")
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
        #logger.info(f"[abmassign.cgi] Funcion: {funcion}")
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
        elif funcion == "pulse":
            s = request_params.get("Segundos", None)
            change_assign_by_name(objeto, 4, s)
            return {"error=0&message=Ok"}
        elif funcion == "get":
            return get_assign(id)
        elif funcion == "delete":
            return delete_assign(id)
        elif funcion == "list":
            return get_assign_list()
        elif funcion == "listall":
            return get_assign_list_all()
        elif funcion == "addassigntoplanta":
            return add_assign_to_planta(id, planta)
        else:
            logger.info(f"[GET abmassign] Función desconocida: {funcion}")
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
        #logger.info(f"[abmassign.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_assign(data)
        elif funcion == "update":
            return update_assign(data)
        else:
            logger.info(f"[POST abmassign] Función desconocida: {funcion}")
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
        #logger.info(f"[abmev.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_event(id)
        elif funcion == "delete":
            return delete_event(id)
        elif funcion == "list":
            return get_event_list()
        elif funcion == "listall":
            return get_event_list_all()
        else:
            logger.info(f"[GET abmev] Función desconocida: {funcion}")
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
        #logger.info(f"[abmev.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_event(data)
        elif funcion == "update":
            return update_event(data)
        else:
            logger.info(f"[POST abmev] Función desconocida: {funcion}")
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
        #logger.info(f"[abmgroup.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_group(id)
        elif funcion == "delete":
            return delete_group(id)
        elif funcion == "list":
            return get_group_list()
        elif funcion == "listall":
            return get_group_list_all()
        else:
            logger.info(f"[GET abmgroup] Función desconocida: {funcion}")
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
        #logger.info(f"[abmgroup.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_group(data)
        elif funcion == "update":
            return update_group(data)
        else:
            logger.info(f"[POST abmgroup] Función desconocida: {funcion}")
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
        #logger.info(f"[abmuser.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_user(id)
        elif funcion == "delete":
            return delete_user(id)
        elif funcion == "list":
            return get_user_list()
        elif funcion == "listall":
            return get_user_list_all()
        else:
            logger.info(f"[GET abmuser] Función desconocida: {funcion}")
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
        #logger.info(f"[abmuser.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_user(data)
        elif funcion == "update":
            return update_user(data)
        else:
            logger.info(f"[POST abmuser] Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}
    

### ABM Task
@router.get("/abmat.cgi")
async def abmat_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    if funcion:
        #logger.info(f"[abmat.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_task(id)
        elif funcion == "delete":
            return delete_task(id)
        elif funcion == "list":
            return get_task_list()
        elif funcion == "listall":
            return get_task_list_all(id)
        else:
            logger.info(f"[GET abmat] Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return get_task_list()
    
@router.post("/abmat.cgi")
async def abmat_post(request: Request):
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
        #logger.info(f"[abmat.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_task(data)
        elif funcion == "update":
            return update_task(data)
        else:
            logger.info(f"[POST abmat] Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}

### ABM Automatizaciones
@router.get("/abmauto.cgi")
async def abmauto_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    tipo = request_params.get("Tipo", None)
    if funcion:
        #logger.info(f"[abmauto.cgi] Funcion: {funcion}")
        id = request_params.get("Id", None)
        if funcion == "get":
            return get_auto(id)
        elif funcion == "delete":
            return delete_auto(id)
        elif funcion == "list":
            return get_auto_list(tipo)
        elif funcion == "listall":
            return get_auto_list_all(tipo)
        else:
            logger.info(f"[GET abmauto] Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return get_auto_list(tipo)
    
@router.post("/abmauto.cgi")
async def abmauto_post(request: Request):
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
        #logger.info(f"[abmauto.cgi] Funcion: {funcion}")
        if funcion == "add":
            return add_auto(data)
        elif funcion == "update":
            return update_auto(data)
        else:
            logger.info(f"[POST abmauto] Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}

### ABM Tactiles
@router.get("/abmtouch.cgi")
async def abmtouch_get(request: Request):
    # Parámetros GET (query string)
    request_params = dict(request.query_params)
    # Headers (variables del navegador)
    headers = dict(request.headers)

    # Me abro por función
    funcion = request_params.get("funcion", None)
    id = request_params.get("Id", None)
    pantalla = request_params.get("Pantalla", None)
    boton = request_params.get("Boton", None)
    if funcion:
        #logger.info(f"[abmtouch.cgi] Funcion: {funcion}")
        if funcion == "get":
            return get_touch(id, pantalla, boton)
        elif funcion == "delete":
            return delete_touch(id, pantalla, boton)
        elif funcion == "list":
            return get_touch_list(id, pantalla)
        elif funcion == "listall":
            return get_touch_list_all()
        elif funcion == "add":
            return add_touch(id, pantalla, boton)
        else:
            logger.info(f"[GET abmtouch] Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return get_touch_list(id, pantalla)
    
@router.post("/abmtouch.cgi")
async def abmtouch_post(request: Request):
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
        #logger.info(f"[abmtouch.cgi] Funcion: {funcion}")
        if funcion == "update":
            return update_touch(data)
        else:
            logger.info(f"[POST abmtouch] Función desconocida: {funcion}")
            return {f"error=3&message=Función desconocida: {funcion}"}
    else:
        return {f"error=3&message=Función no informada"}

### Configuracion de HW
@router.get("/hwconfig.cgi")
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

@router.post("/hwconfig.cgi")
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
        logger.info(f"[hwconfig.cgi] Funcion: {funcion}")

    return {f"error=0&message=Ok"}
