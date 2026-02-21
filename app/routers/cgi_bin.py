from fastapi import APIRouter, Request, Form
from app.log_utils import get_daily_logger
from app.config_utils import get_config_value
from app.mysql_utils import mysql_connect, mysql_disconnect, mysql_execute, mysql_query

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

    #DBHOST=192.168.10.32
    #DBNAME=DB_DOMPIWEB
    #DBUSER=dompi_web
    #DBPASSWORD=dompi_web
    db_host = get_config_value("/app/etc/dompiweb.conf", "DBHOST")
    db_name = get_config_value("/app/etc/dompiweb.conf", "DBNAME")
    db_user = get_config_value("/app/etc/dompiweb.conf", "DBUSER")
    db_password = get_config_value("/app/etc/dompiweb.conf", "DBPASSWORD")
    logger.info(f"DB Config: host={db_host} name={db_name} user={db_user} password={'*' * len(db_password) if db_password else None}")

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
    conn = mysql_connect(db_host, db_name, db_user, db_password)
    if conn:
        logger.info("Conexión a MySQL exitosa")
        # Ejemplo: insertar un log de la petición
        query_result = mysql_query(conn, "SELECT * FROM TB_DOM_PERIF WHERE MAC = %s;", (data.get("ID", "NULL").upper(),))
        mysql_disconnect(conn)
        logger.info(f"Query result: {query_result}")
        if query_result:
            logger.info("Periférico encontrado")
            return {"error=0&message=Ok"}
        else:
            logger.info("Periférico no encontrado")
            return {"error=2&message=Periférico no existe"}
    else:
        logger.error("No se pudo conectar a MySQL")
        return {"error=1&message=Error de conexion a la base de datos"}




