from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

"""
CREATE TABLE IF NOT EXISTS TB_DOM_USER (
Id integer primary key,
Usuario varchar(16) NOT NULL,         -- Nombre corto (1 palabra)
Nombre_Completo varchar(64) NOT NULL,        -- Nombre completo
Pin_Teclado varchar(32),
Pin_SMS varchar(32),
Pin_WEB varchar(32),
Telefono_Voz varchar(32),
Telefono_SMS varchar(32),
Usuario_Cloud varchar(256),
Clave_Cloud varchar(256),
Amazon_Key varchar(256),
Google_Key varchar(256),
Apple_Key varchar(256),
Other_Key varchar(256),
Tarjeta varchar(256),
Acceso_Fisico varchar(256),     -- Id de Puertas de acceso separadas por , (comas)
Acceso_Web varchar(256),
Acceso_Clowd varchar(256),
Dias_Semana varchar(128),
Hora_Desde integer DEFAULT 0,
Minuto_Desde integer DEFAULT 0,
Hora_Hasta integer DEFAULT 0,
Minuto_Hasta integer DEFAULT 0,
Estado varchar(32), -- Habilitado, Bloqueado [motivo]
Contador_Error integer DEFAULT 0,
Ultimo_Acceso varchar(32),
Ultimo_Error varchar(32),
Flags integer DEFAULT 0,
UNIQUE INDEX idx_user_id (Id)
);
"""

def get_user_list():
    query_result = mysql_query("SELECT Id, Usuario, Nombre_Completo, Estado, Ultimo_Acceso FROM TB_DOM_USER ORDER BY Usuario ASC;");
    return {"error": 0, "message": "Ok", "response": query_result}

def get_user_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_USER")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_user(id):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_USER WHERE Id = {id}")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_user(data):
    next_id = mysql_next_id('TB_DOM_USER')
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
    query = f"INSERT INTO TB_DOM_USER ({campos_str}) VALUES ({valores_str})"

    #logger.info(f"[add_user] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_user(data):
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
    query = f"UPDATE TB_DOM_USER SET {campos_valores_str} WHERE Id = {Id}"

    #logger.info(f"[update_user] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_user(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_USER WHERE Id = {Id}"
    #logger.info(f"[delete_user] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}
