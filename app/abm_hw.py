from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

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

def check_hw(mac_addr, ip_address, info):
    # Verificar si el periférico ya existe
    if mac_addr != None:
        query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE MAC = '{mac_addr}'")
    else:
        query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE Direccion_IP = '{ip_address}'")

    if query_result:
        if query_result[0]["Estado"] == 0:
            logger.info(f"HW: {query_result[0]['Dispositivo']} OFFLINE -> ONLINE")
        # Actualizar el periférico existente
        mysql_execute(f"UPDATE TB_DOM_PERIF SET Direccion_IP = '{ip_address}', Ultimo_Ok = UNIX_TIMESTAMP(), Estado = 1, Informacion = '{info}' WHERE MAC = '{mac_addr}'")
        return query_result[0]['Id'] 
    else:
        # HW no existe
        return None

def get_hardware_list():
    query_result = mysql_query("SELECT Id, Dispositivo, Tipo, Estado FROM TB_DOM_PERIF ORDER BY Dispositivo ASC")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_hardware_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_PERIF")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_hardware(id):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE Id = {id}")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_hardware(data):
    next_id = mysql_next_id('TB_DOM_PERIF')
    if next_id in (None, ''):
        next_id = 1
    data['Id'] = next_id

    campos = []
    valores = []
    for key, value in data.items():
        campos.append(key)
        if isinstance(value, str):
            escaped_value = value.replace("'", "''")
            valores.append(f"'{escaped_value}'")
        else:
            valores.append(str(value))

    campos_str = ', '.join(campos)
    valores_str = ', '.join(valores)
    query = f"INSERT INTO TB_DOM_PERIF ({campos_str}) VALUES ({valores_str})"

    logger.info(f"[add_hardware] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_hardware(data):
    Id = data.get('Id')
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    campos_valores = []
    for key, value in data.items():
        if key == 'Id':
            continue
        if isinstance(value, str):
            escaped_value = value.replace("'", "''")
            campos_valores.append(f"{key} = '{escaped_value}'")
        else:
            campos_valores.append(f"{key} = {value}")

    campos_valores_str = ', '.join(campos_valores)
    query = f"UPDATE TB_DOM_PERIF SET {campos_valores_str} WHERE Id = {Id}"

    logger.info(f"[update_hardware] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_hardware(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_PERIF WHERE Id = {Id}"
    logger.info(f"[delete_hardware] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}
