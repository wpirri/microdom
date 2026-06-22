from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

"""
CREATE TABLE IF NOT EXISTS TB_DOM_GROUP (
Id integer primary key,
Grupo varchar(128) NOT NULL,
Listado_Objetos varchar(256),       -- Id de assign separados por , (comas)
Estado integer DEFAULT 0,            -- Define el estado que deben tener los objetos del grupo
Icono_Apagado varchar(32),
Icono_Encendido varchar(32),
Grupo_Visual integer DEFAULT 0,             -- 0=Ninguno 1=Alarma 2=Iluminación 3=Puertas 4=Climatización 5=Cámaras 6=Riego
Planta integer DEFAULT 0,
Cord_x integer DEFAULT 0,
Cord_y integer DEFAULT 0,
Actualizar integer DEFAULT 0,
UNIQUE INDEX idx_group_id (Id)
);
"""

def get_group_list():
    query_result = mysql_query("SELECT Id, Grupo FROM TB_DOM_GROUP ORDER BY Grupo ASC;");
    return {"error": 0, "message": "Ok", "response": query_result}

def get_group_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_GROUP")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_group(id):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_GROUP WHERE Id = {id}")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_group(data):
    next_id = mysql_next_id('TB_DOM_GROUP')
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
    query = f"INSERT INTO TB_DOM_GROUP ({campos_str}) VALUES ({valores_str})"

    #logger.info(f"[add_group] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_group(data):
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
    query = f"UPDATE TB_DOM_GROUP SET {campos_valores_str} WHERE Id = {Id}"

    #logger.info(f"[update_group] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_group(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_GROUP WHERE Id = {Id}"
    #logger.info(f"[delete_group] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def change_group_by_id(id, accion):
    estado = 0

    return estado
