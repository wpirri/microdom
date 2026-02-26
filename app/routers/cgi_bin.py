from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.config_utils import get_config_value
from app.mysql_utils import mysql_execute, mysql_query

logger = get_daily_logger("microdom", "/app/logs/microdom.log")

router = APIRouter(prefix="/cgi-bin", tags=["cgi"])

@router.post("/infoio.cgi")
async def infoio(request: Request):
    # 1. Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)
    #logger.info(f"[infoio.cgi] FORM={data}")
    hw_mac_addr = data.get("ID", "NULL").upper()

    # 2. Leer parámetros GET (query string)
    #request_params = dict(request.query_params)
    #logger.info("[infoio.cgi] GET params: %s", request_params)

    # 3. Leer headers (variables del navegador)
    #headers = dict(request.headers)
    #logger.info("[infoio.cgi] Headers: %s", headers)

    """
        CREATE TABLE IF NOT EXISTS TB_DOM_PERIF (
            Id integer primary key,
            MAC varchar(16) NOT NULL,                       -- MAC Address
            Dispositivo varchar(128) NOT NULL,
            Tipo integer DEFAULT 0,                         -- 0=Ninguno, 1=Wifi 2=RBPi 3=DSC 4=Garnet
            Estado integer DEFAULT 0,                       -- 0=Offline
            Direccion_IP varchar(16) DEFAULT "0.0.0.0",
            Ultimo_Ok integer DEFAULT 0,
            Usar_Https integer DEFAULT 0,
            Habilitar_Wiegand integer DEFAULT 0,
            Update_Firmware integer DEFAULT 0,
            Update_WiFi integer DEFAULT 0,
            Update_Config integer DEFAULT 0,
            Informacion varchar(1024),
            UNIQUE INDEX idx_perif_id (Id),
            UNIQUE INDEX idx_perif_mac (MAC)
        );
    """
    # Busco el dispositivo por MAC
    query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE MAC = '{hw_mac_addr}';")
    #logger.info(f"Query result: {query_result}")
    if query_result:
        #logger.info("Periférico encontrado")



        
        return {"error=0&message=Ok"}
    else:
        logger.info(f"Periférico {hw_mac_addr} no encontrado")
        return {f"error=2&message=HW {hw_mac_addr} no encontrado"}


@router.get("/abmassign.cgi")
async def abmassign(request: Request):
    # 1. Leer el POST
    #form = await request.form()   # ← parsea x-www-form-urlencoded
    #data = dict(form)
    #logger.info(f"[abmassign.cgi] FORM={data}")

    # 2. Leer parámetros GET (query string)
    request_params = dict(request.query_params)
    logger.info("[abmassign.cgi] GET params: %s", request_params)

    # 3. Leer headers (variables del navegador)
    headers = dict(request.headers)
    logger.info("[abmassign.cgi] Headers: %s", headers)
    raddr = headers.get("host", "255.255.255.255")
    # Busco el dispositivo por IP
    query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE Direccion_IP = '{raddr}';")
    #logger.info(f"Query result: {query_result}")
    if query_result:
        #logger.info("Periférico encontrado")



        
        return {"error=0&message=Ok"}
    else:
        logger.info(f"Periférico {raddr} no encontrado")
        return {f"error=2&message=HW {raddr} no encontrado"}
